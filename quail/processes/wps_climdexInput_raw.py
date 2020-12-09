import os
from rpy2 import robjects
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, Format
from pywps.app.Common import Metadata
from tempfile import NamedTemporaryFile

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import (
    tmax_column,
    tmin_column,
    prec_column,
    base_range,
    na_strings,
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
)


class ClimdexInputRaw(Process):
    """
    Process for creating climdexInput object from data already ingested into R
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "load_rdata": 10,
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
                min_occurs=0,
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
                default="tmax",
                abstract="Name of R object containing daily minimum temperature data.",
                data_type="string",
            ),
            LiteralInput(
                "prec_name",
                "daily total precipitation data file",
                default="tmax",
                abstract="Name of R object containing daily mean temperature data.",
                data_type="string",
            ),
            LiteralInput(
                "tavg_name",
                "mean temperature data file",
                default="tmax",
                abstract="Name of R object containing daily total precipitation data.",
                data_type="string",
            ),
            tmax_column,
            tmin_column,
            prec_column,
            base_range,
            na_strings,
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
            log_level,
        ]

        outputs = [
            ComplexOutput(
                "climdexInput",
                "generated climdexInput",
                abstract="Output R data file for generated climdexInput",
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64")
                ],
            ),
        ]

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

    def collect_literal_inputs(self, request):
        return [
            arg[0] for arg in list(collect_args(request, self.workdir).values())[-21:]
        ]

    def generate_dates(
        self, request, filename, obj_name, date_fields, date_format, cal
    ):
        load_rdata_to_python(filename, obj_name)
        return robjects.r(
            f"as.PCICt(do.call(paste, {obj_name}[,{date_fields}]), format={date_format}, cal={cal})"
        )

    def _handler(self, request, response):
        (
            tmax_name,
            tmin_name,
            prec_name,
            tavg_name,
            tmax_column,
            tmin_column,
            prec_column,
            base_range,
            na_strings,
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
            loglevel,
        ) = self.collect_literal_inputs(request)

        climdex = get_package("climdex.pcic")
        robjects.r("library(PCICt)")

        tmax_file = collect_args(request, self.workdir)["tmax_file"][0]
        tmin_file = collect_args(request, self.workdir)["tmin_file"][0]
        prec_file = collect_args(request, self.workdir)["prec_file"][0]

        tmax_dates = self.generate_dates(
            request, tmax_file, tmax_name, date_fields, date_format, cal
        )
        tmin_dates = self.generate_dates(
            request, tmin_file, tmin_name, date_fields, date_format, cal
        )
        prec_dates = self.generate_dates(
            request, prec_file, prec_name, date_fields, date_format, cal
        )

        tmax = robjects.r(f"{tmax_name}${tmax_column}")
        tmin = robjects.r(f"{tmin_name}${tmin_column}")
        prec = robjects.r(f"{prec_name}${prec_column}")

        ci = climdex.climdexInput_raw(
            tmax, tmin, prec, tmax_dates, tmin_dates, prec_dates
        )

        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata("ci", ci, output_path)

        response.outputs["climdexInput"].file = output_path

        # Clear R global env
        robjects.r("rm(list=ls())")

        return response
