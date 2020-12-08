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
                default='list(tmin = "tmin", tmax = "tmax", prec = "prec")',
                abstract="Column names for tmin, tmax, and prec data.",
                data_type="string",
            ),
            LiteralInput(
                "base_range",
                "basline range",
                default="c(1961, 1990)",
                abstract="Years to use for the baseline",
                data_type="string",
            ),
            LiteralInput(
                "na_strings",
                "NA strings",
                abstract="Strings used for NA values",
                default="NULL",
                data_type="string",
            ),
            LiteralInput(
                "cal",
                "calendar type",
                default="gregorian",
                abstract="The calendar type used in the input files.",
                data_type="string",
            ),
            LiteralInput(
                "date_fields",
                "date fields",
                default="c('year'', 'jday')",
                abstract="Vector of names consisting of the columns to be concatenated together with spaces.",
                data_type="string",
            ),
            LiteralInput(
                "date_format",
                "date format",
                default="%Y %j",
                abstract="Date format as taken by strptime.",
                data_type="string",
            ),
            LiteralInput(
                "n",
                "number of days",
                default=5,
                abstract="Number of days to use as window for daily quantiles.",
                data_type="integer",
            ),
            LiteralInput(
                "northern_hemisphere",
                "number of days",
                default=True,
                abstract="Number of days to use as window for daily quantiles.",
                data_type="boolean",
            ),
            LiteralInput(
                "quantiles",
                "threshold quantiles",
                abstract="Threshold quantiles for supplied variables.",
                default="NULL",
                data_type="string",
            ),
            LiteralInput(
                "temp_qtiles",
                "precipitation quantiles",
                default="c(0.1, 0.9)",
                abstract="Quantiles to calculate for temperature variables",
                data_type="string",
            ),
            LiteralInput(
                "prec_qtiles",
                "temperature quantiles",
                default="c(0.95, 0.99)",
                abstract="Quantiles to calculate for precipitation",
                data_type="string",
            ),
            LiteralInput(
                "max_missing_days",
                "maximum missing days",
                default="c(annual = 15, monthly =3)",
                abstract="Vector containing thresholds for number of days allowed missing per year (annual) and per month (monthly).",
                data_type="string",
            ),
            LiteralInput(
                "min_base_data_fraction_present",
                "minimum fraction of base data",
                default=0.1,
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

    def collect_literal_inputs(self, request):
        return [
            arg[0] for arg in list(collect_args(request, self.workdir).values())[-14:]
        ]

    def _handler(self, request, response):
        (
            data_columns,
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
            loglevel,
        ) = self.collect_literal_inputs(request)
        print(data_columns)

        return response
