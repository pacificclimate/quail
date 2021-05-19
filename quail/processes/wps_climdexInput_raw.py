import os
from rpy2 import robjects
from pywps import Process
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.R import (
    get_package,
    save_python_to_rdata,
    r_valid_name,
)
from wps_tools import process_inputs_alpha

from quail.utils import logger, validate_vectors, get_robj
from quail.io import raw_inputs, ci_output


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

        inputs = raw_inputs
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
        df = get_robj(filename, obj_name)
        robjects.r.assign(obj_name, df)

        try:
            return robjects.r(
                f"as.PCICt(do.call(paste, {obj_name}[,{date_fields}]), format='{date_format}', cal='{cal}')"
            )
        except RRuntimeError as e:
            raise ProcessError(msg=f"{type(e).__name__}: Error generating dates")

    def column(self, df_name, column_name, var):
        df_column = robjects.r(df_name).rx2(column_name)
        if robjects.r["is.null"](df_column)[0]:
            raise ProcessError(f"No {var} column of that name")
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
        prec_file,
        tavg_file,
        tmax_file,
        tmin_file,
    ):
        prec_dates = self.generate_dates(
            request, prec_file, prec_name, date_fields, date_format, cal
        )
        prec = self.column(prec_name, prec_column, "prec")

        if tavg_file:
            # use tavg data if provided
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

        elif tmax_file and tmin_file:
            # use tmax and tmin data if tavg is not provided
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
            base_range,
            cal,
            date_fields,
            date_format,
            loglevel,
            max_missing_days,
            min_base_data_fraction_present,
            n,
            northern_hemisphere,
            output_file,
            prec_column,
            prec_file,
            prec_name,
            prec_qtiles,
            quantiles,
            tavg_column,
            tavg_file,
            tavg_name,
            temp_qtiles,
            tmax_column,
            tmax_file,
            tmax_name,
            tmin_column,
            tmin_file,
            tmin_name,
            vector_name,
        ) = process_inputs_alpha(request.inputs, raw_inputs, self.workdir)

        validate_vectors(
            [
                base_range,
                date_fields,
                temp_qtiles,
                prec_qtiles,
                max_missing_days,
            ]
        )

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
            prec_file,
            tavg_file,
            tmax_file,
            tmin_file,
        )

        log_handler(
            self,
            response,
            "Processing climdexInput.raw",
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
            raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

        log_handler(
            self,
            response,
            "Saving climdexInput as R data file",
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
