from rpy2 import robjects
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, Format
from pywps.app.Common import Metadata
from tempfile import NamedTemporaryFile

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python
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


class ClimdexInputCSV(Process):
    """
    Process for creating climdexInput object from CSV files
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
                min_occurs=0,
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

    def collect_literal_inputs(self, request):
        return [
            arg[0] for arg in list(collect_args(request, self.workdir).values())[-17:]
        ]

    def _handler(self, request, response):
        (
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

        return response
