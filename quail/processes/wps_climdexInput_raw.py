import os
from rpy2 import robjects
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, Format
from pywps.app.Common import Metadata
from tempfile import NamedTemporaryFile
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, collect_args, rda_output, vector_name
from wps_tools.R import get_package, load_rdata_to_python, save_python_to_rdata
from quail.utils import (
    logger,
    collect_literal_inputs,
    load_rda,
    r_valid_name,
    validate_vector,
)
from quail.io import (
    tmax_column,
    tmin_column,
    prec_column,
    tavg_column,
    base_range,
    cal,
    date_fields,
    date_format,
    n,
    northern_hemisphere,
    quantiles,
    temp_qtiles,
    prec_qtiles,
    max_missing_days,
    min_base_data_fraction_present,
    output_file,
    ci_output,
)


class ClimdexInputRaw(Process):
    """
    Process for creating climdexInput object from data already ingested into R
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "prepare_params": 10,
                "save_rdata": 90,
            },
        )
        inputs = [
            ComplexInput(
                "tmax_file",
                "daily maximum temperature data file",
                abstract="Name of file containing daily maximum temperature data.",
                min_occurs=0,
                max_occurs=1,
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64"),
                ],
            ),
            ComplexInput(
                "tmin_file",
                "daily minimum temperature data file",
                abstract="Name of file containing daily minimum temperature data.",
                min_occurs=0,
                max_occurs=1,
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64"),
                ],
            ),
            ComplexInput(
                "prec_file",
                "daily total precipitation data file",
                abstract="Name of file containing daily total precipitation data.",
                min_occurs=1,
                max_occurs=1,
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64"),
                ],
            ),
            ComplexInput(
                "tavg_file",
                "mean temperature data file",
                abstract="Name of file containing daily mean temperature data.",
                min_occurs=0,
                max_occurs=1,
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64"),
                ],
            ),
            LiteralInput(
                "tmax_name",
                "daily maximum temperature object name",
                default="tmax",
                abstract="Name of R object containing daily maximum temperature data.",
                data_type="string",
            ),
            LiteralInput(
                "tmin_name",
                "daily minimum temperature data file",
                default="tmin",
                abstract="Name of R object containing daily minimum temperature data.",
                data_type="string",
            ),
            LiteralInput(
                "prec_name",
                "daily total precipitation data file",
                default="prec",
                abstract="Name of R object containing daily mean temperature data.",
                data_type="string",
            ),
            LiteralInput(
                "tavg_name",
                "mean temperature data file",
                default="tavg",
                abstract="Name of R object containing daily total precipitation data.",
                data_type="string",
            ),
            tmax_column,
            tmin_column,
            prec_column,
            tavg_column,
            base_range,
            cal,
            date_fields,
            date_format,
            n,
            northern_hemisphere,
            quantiles,
            temp_qtiles,
            prec_qtiles,
            max_missing_days,
            min_base_data_fraction_present,
            output_file,
            vector_name,
            log_level,
        ]

        outputs = [ci_output]

        super(ClimdexInputRaw, self).__init__(
            self._handler,
            identifier="climdex_input_raw",
            title="climdexInput generator (raw)",
            abstract="Process for creating climdexInput object from data already ingested into R",
            metadata=[
                Metadata("NetCDF processing"),
                Metadata("Climate Data Operations"),
                Metadata("PyWPS", "https://pywps.org/"),
                Metadata("Birdhouse", "http://bird-house.github.io/"),
                Metadata("PyWPS Demo", "https://pywps-demo.readthedocs.io/en/latest/"),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
        )

    def generate_dates(
        self, request, filename, obj_name, date_fields, date_format, cal
    ):
        load_rda(filename, obj_name)
        try:
            return robjects.r(
                f"as.PCICt(do.call(paste, {obj_name}[,{date_fields}]), format='{date_format}', cal='{cal}')"
            )
        except RRuntimeError as e:
            raise ProcessError(msg="Error generating dates")

    def column(self, df_name, column_name, var):
        df_column = robjects.r(df_name).rx2(column_name)
        if robjects.r["is.null"](df_column)[0]:
            raise ProcessError(f"RRuntimeError: No {var} column of that name")
        else:
            return df_column

    def prepare_parameters(
        self,
        request,
        tmax_name,
        tmin_name,
        prec_name,
        tavg_name,
        tmax_column,
        tmin_column,
        prec_column,
        tavg_column,
        date_fields,
        date_format,
        cal,
    ):
        args = collect_args(request, self.workdir)
        prec_file = args["prec_file"][0]
        prec_dates = self.generate_dates(
            request, prec_file, prec_name, date_fields, date_format, cal
        )
        prec = self.column(prec_name, prec_column, "prec")

        if "tavg_file" in args.keys():
            # use tavg data if provided
            tavg_file = args["tavg_file"][0]
            tavg_dates = self.generate_dates(
                request, tavg_file, tavg_name, date_fields, date_format, cal
            )
            tavg = self.column(tavg_name, tavg_column, "tavg")

            return {
                "tavg": tavg,
                "prec": prec,
                "tavg_dates": tavg_dates,
                "prec_dates": prec_dates,
            }

        elif "tmax_file" in args.keys() and "tmin_file" in args.keys():
            # use tmax and tmin data if tavg is not provided
            tmax_file = args["tmax_file"][0]
            tmin_file = args["tmin_file"][0]

            tmax_dates = self.generate_dates(
                request, tmax_file, tmax_name, date_fields, date_format, cal
            )
            tmin_dates = self.generate_dates(
                request, tmin_file, tmin_name, date_fields, date_format, cal
            )

            tmax = self.column(tmax_name, tmax_column, "tmax")
            tmin = self.column(tmin_name, tmin_column, "tmin")

            return {
                "tmax": tmax,
                "tmin": tmin,
                "prec": prec,
                "tmax_dates": tmax_dates,
                "tmin_dates": tmin_dates,
                "prec_dates": prec_dates,
            }

    def _handler(self, request, response):
        (
            tmax_name,
            tmin_name,
            prec_name,
            tavg_name,
            tmax_column,
            tmin_column,
            prec_column,
            tavg_column,
            base_range,
            cal,
            date_fields,
            date_format,
            n,
            northern_hemisphere,
            quantiles,
            temp_qtiles,
            prec_qtiles,
            max_missing_days,
            min_base_data_fraction_present,
            output_file,
            vector_name,
            loglevel,
        ) = collect_literal_inputs(request)
        [
            validate_vector(vector)
            for vector in [
                base_range,
                date_fields,
                temp_qtiles,
                prec_qtiles,
                max_missing_days,
            ]
        ]

        log_handler(
            self,
            response,
            "Starting Process",
            logger,
            log_level=loglevel,
            process_step="start",
        )
        climdex = get_package("climdex.pcic")
        robjects.r("library(PCICt)")

        log_handler(
            self,
            response,
            "Prepare parameters for climdexInput.raw",
            logger,
            log_level=loglevel,
            process_step="prepare_params",
        )
        params = self.prepare_parameters(
            request,
            tmax_name,
            tmin_name,
            prec_name,
            tavg_name,
            tmax_column,
            tmin_column,
            prec_column,
            tavg_column,
            date_fields,
            date_format,
            cal,
        )

        log_handler(
            self,
            response,
            f"Processing climdexInput.raw",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        try:
            ci = climdex.climdexInput_raw(
                **params,
                base_range=robjects.r(base_range),
                n=n,
                northern_hemisphere=northern_hemisphere,
                quantiles=robjects.r(quantiles),
                temp_qtiles=robjects.r(temp_qtiles),
                prec_qtiles=robjects.r(prec_qtiles),
                max_missing_days=robjects.r(max_missing_days),
                min_base_data_fraction_present=min_base_data_fraction_present,
            )
        except RRuntimeError as e:
            err_msg = type(e).__name__ + ": " + str(e)
            raise ProcessError(msg=err_msg)

        log_handler(
            self,
            response,
            f"Saving climdexInput as R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        r_valid_name(vector_name)
        save_python_to_rdata(vector_name, ci, output_path)

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )
        response.outputs["climdexInput"].file = output_path

        # Clear R global env
        robjects.r("rm(list=ls())")

        return response
