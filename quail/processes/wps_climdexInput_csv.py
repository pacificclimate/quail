import os, csv
from rpy2 import robjects
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, Format
from pywps.app.Common import Metadata
from tempfile import NamedTemporaryFile
from pywps.app.exceptions import ProcessError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, collect_args, rda_output, vector_name
from wps_tools.R import get_package, load_rdata_to_python, save_python_to_rdata
from quail.utils import logger, collect_literal_inputs, r_valid_name, validate_vector
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


class ClimdexInputCSV(Process):
    """
    Process for creating climdexInput object from CSV files
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
                    Format("text/csv", extension=".csv"),
                ],
            ),
            ComplexInput(
                "tmin_file",
                "daily minimum temperature data file",
                abstract="Name of file containing daily minimum temperature data.",
                min_occurs=0,
                max_occurs=1,
                supported_formats=[
                    Format("text/csv", extension=".csv"),
                ],
            ),
            ComplexInput(
                "prec_file",
                "daily total precipitation data file",
                abstract="Name of file containing daily total precipitation data.",
                min_occurs=1,
                max_occurs=1,
                supported_formats=[
                    Format("text/csv", extension=".csv"),
                ],
            ),
            ComplexInput(
                "tavg_file",
                "mean temperature data file",
                abstract="Name of file containing daily mean temperature data.",
                min_occurs=0,
                max_occurs=1,
                supported_formats=[
                    Format("text/csv", extension=".csv"),
                ],
            ),
            LiteralInput(
                "na_strings",
                "climdexInput name",
                abstract="Strings used for NA values; passed to read.csv",
                default="NULL",
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

        super(ClimdexInputCSV, self).__init__(
            self._handler,
            identifier="climdex_input_csv",
            title="climdexInput generator (CSV)",
            abstract="Process for creating climdexInput object from CSV files",
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

    def check_columns(self, csv_file, column, var):
        with open(csv_file, "r") as file_:
            reader = csv.reader(file_)
            columns = next(reader)
            if column not in columns:
                raise ProcessError(f"RRuntimeError: No {var} column of that name")

    def prepare_parameters(
        self,
        request,
        date_fields,
        date_format,
        tmax_column,
        tmin_column,
        prec_column,
        tavg_column,
    ):
        args = collect_args(request, self.workdir)
        prec_file = args["prec_file"][0]
        self.check_columns(prec_file, prec_column, "prec")
        data_types = robjects.r(
            f"list(list(fields={date_fields}, format='{date_format}'))"
        )

        if "tavg_file" in args.keys():
            # use tavg data if provided
            tavg_file = prec_file = args["tavg_file"][0]
            self.check_columns(tavg_file, tavg_column, "tavg")
            date_columns = robjects.r(
                f"list(tavg = '{tavg_column}', prec = '{prec_column}')"
            )
            return {
                "tavg_file": tavg_file,
                "prec_file": prec_file,
                "data_columns": date_columns,
                "date_types": data_types,
            }

        elif "tmax_file" in args.keys() and "tmin_file" in args.keys():
            # use tmax and tmin data if tavg is not provided
            tmax_file = args["tmax_file"][0]
            self.check_columns(tmax_file, tmax_column, "tmax")
            tmin_file = args["tmin_file"][0]
            self.check_columns(tmin_file, tmin_column, "tmin")

            date_columns = robjects.r(
                f"list(tmax = '{tmax_column}', tmin = '{tmin_column}', prec = '{prec_column}')"
            )
            return {
                "tmax_file": tmax_file,
                "tmin_file": tmin_file,
                "prec_file": prec_file,
                "data_columns": date_columns,
                "date_types": data_types,
            }

    def _handler(self, request, response):
        (
            na_strings,
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
            "Prepare parameters for climdexInput.csv",
            logger,
            log_level=loglevel,
            process_step="prepare_params",
        )
        params = self.prepare_parameters(
            request,
            date_fields,
            date_format,
            tmax_column,
            tmin_column,
            prec_column,
            tavg_column,
        )

        log_handler(
            self,
            response,
            f"Processing climdexInput.csv",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        try:
            ci = climdex.climdexInput_csv(
                **params,
                base_range=robjects.r(base_range),
                na_strings=na_strings,
                cal=robjects.r(f"'{cal}'"),
                n=n,
                northern_hemisphere=northern_hemisphere,
                quantiles=robjects.r(quantiles),
                temp_qtiles=robjects.r(temp_qtiles),
                prec_qtiles=robjects.r(prec_qtiles),
                max_missing_days=robjects.r(max_missing_days),
                min_base_data_fraction_present=min_base_data_fraction_present,
            )
        except RRuntimeError as e:
            raise ProcessError(msg=str(e))

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
