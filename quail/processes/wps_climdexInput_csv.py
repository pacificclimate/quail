import os, csv
from rpy2 import robjects
from tempfile import NamedTemporaryFile as TempFile
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.R import get_package, save_python_to_rdata, r_valid_name

from quail.utils import logger, validate_vectors, process_inputs
from quail.io import climdexInput_csv_inputs, ci_output


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
        inputs = climdexInput_csv_inputs
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

    def prepare_csv_files(
        self, prec_file_content, tavg_file_content, tmax_file_content, tmin_file_content
    ):
        def write_csv(content):
            file_ = TempFile(mode="w+", suffix=".csv")
            file_.write(content)
            file_.seek(0)

            return file_

        prec_file = write_csv(prec_file_content)

        if tavg_file_content:
            tavg_file = write_csv(tavg_file_content)
            return {"prec_file": prec_file, "tavg_file": tavg_file}

        elif tmax_file_content and tmin_file_content:
            tmax_file = write_csv(tmax_file_content)
            tmin_file = write_csv(tmin_file_content)
            return {
                "prec_file": prec_file,
                "tmin_file": tmin_file,
                "tmax_file": tmax_file,
            }

        else:
            raise ProcessError(
                "You must provide one of either a tavg file content or tmax and tmin file content"
            )

    def prepare_parameters(
        self,
        data_files,
        date_fields,
        date_format,
        tmax_column,
        tmin_column,
        prec_column,
        tavg_column,
    ):
        def check_columns(csv_file, column, var):
            with open(csv_file, "r") as file_:
                reader = csv.reader(file_)
                columns = next(reader)
                if column not in columns:
                    raise ProcessError(f"No {var} column of that name")

        prec_file = data_files["prec_file"]
        check_columns(prec_file.name, prec_column, "prec")
        data_types = robjects.r(
            f"list(list(fields={date_fields}, format='{date_format}'))"
        )

        if "tavg_file" in data_files.keys():
            # use tavg data if provided
            tavg_file = data_files["tavg_file"]
            check_columns(tavg_file.name, tavg_column, "tavg")
            date_columns = robjects.r(
                f"list(tavg = '{tavg_column}', prec = '{prec_column}')"
            )
            return {
                "tavg_file": tavg_file,
                "prec_file": prec_file,
                "data_columns": date_columns,
                "date_types": data_types,
            }

        elif "tmax_file" in data_files.keys() and "tmin_file" in data_files.keys():
            # use tmax and tmin data if tavg is not provided
            tmax_file = data_files["tmax_file"]
            check_columns(tmax_file.name, tmax_column, "tmax")
            tmin_file = data_files["tmin_file"]
            check_columns(tmin_file.name, tmin_column, "tmin")

            date_columns = robjects.r(
                f"list(tmax = '{tmax_column}', tmin = '{tmin_column}', prec = '{prec_column}')"
            )
            return {
                "tmax_file": tmax_file.name,
                "tmin_file": tmin_file.name,
                "prec_file": prec_file.name,
                "data_columns": date_columns,
                "date_types": data_types,
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
            na_strings,
            northern_hemisphere,
            output_file,
            prec_column,
            prec_file_content,
            prec_qtiles,
            quantiles,
            tavg_column,
            tavg_file_content,
            temp_qtiles,
            tmax_column,
            tmax_file_content,
            tmin_column,
            tmin_file_content,
            vector_name,
        ) = process_inputs(request.inputs, climdexInput_csv_inputs, self.workdir)

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
            "Prepare parameters for climdexInput.csv",
            logger,
            log_level=loglevel,
            process_step="prepare_params",
        )

        data_files = self.prepare_csv_files(
            prec_file_content, tavg_file_content, tmax_file_content, tmin_file_content
        )
        params = self.prepare_parameters(
            data_files,
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
            raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

        finally:
            [tmpfile.close() for tmpfile in data_files.values()]

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
