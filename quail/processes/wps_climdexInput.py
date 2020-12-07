from rpy2 import robjects
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, Format
from pywps.app.Common import Metadata
from tempfile import NamedTemporaryFile

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger


class ClimdexInput(Process):
    """
    Process for creating climdexInput object from CSV/rda files
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "build_rdata": 90,
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
                    Format("application/x-gzip", extension=".rda", encoding="base64"),
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
                    Format("application/x-gzip", extension=".rda", encoding="base64"),
                    Format("text/csv", extension=".csv"),
                ],
            ),
            ComplexInput(
                "tvag_file",
                "mean temperature data file",
                abstract="Name of file containing daily mean temperature data.",
                min_occurs=0,
                max_occurs=1,
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64"),
                    Format("text/csv", extension=".csv"),
                ],
            ),
            LiteralInput(
                "data_columns",
                "data columns",
                abstract="Column names for tmin, tmax, and prec data.",
                data_type="string",
            ),
            LiteralInput(
                "base_range",
                "basline range",
                abstract="Years to use for the baseline",
                data_type="string",
            ),
            LiteralInput(
                "na_strings",
                "NA strings",
                abstract="Strings used for NA values",
                min_occurs=0,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "cal",
                "calendar type",
                abstract="The calendar type used in the input files.",
                data_type="string",
            ),
            LiteralInput(
                "date_fields",
                "date fields",
                abstract="Vector of names consisting of the columns to be concatenated together with spaces.",
                data_type="string",
            ),
            LiteralInput(
                "date_format",
                "date format",
                abstract="Date format as taken by strptime.",
                data_type="string",
            ),
            LiteralInput(
                "n",
                "number of days",
                abstract="Number of days to use as window for daily quantiles.",
                data_type="integer",
            ),
            LiteralInput(
                "northern_hemisphere",
                "number of days",
                abstract="Number of days to use as window for daily quantiles.",
                data_type="boolean",
            ),
            LiteralInput(
                "quantiles",
                "threshold quantiles",
                abstract="Threshold quantiles for supplied variables.",
                min_occurs=0,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "temp_qtiles",
                "precipitation quantiles",
                abstract="Quantiles to calculate for temperature variables",
                data_type="string",
            ),
            LiteralInput(
                "prec_qtiles",
                "temperature quantiles",
                abstract="Quantiles to calculate for precipitation",
                data_type="string",
            ),
            LiteralInput(
                "max_missing_days",
                "maximum missing days",
                abstract="Vector containing thresholds for number of days allowed missing per year (annual) and per month (monthly).",
                data_type="string",
            ),
            LiteralInput(
                "min_base_data_fraction_present",
                "minimum fraction of base data",
                abstract="Minimum fraction of base data that must be present for quantile to be calculated for a particular day",
                data_type="float",
            ),
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

        super(ClimdexInput, self).__init__(
            self._handler,
            identifier="climdex_input",
            title="climdexInput generator",
            abstract="Process for creating climdexInput object from CSV/rda files",
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

    def _handler(self, request, response):

        return response
