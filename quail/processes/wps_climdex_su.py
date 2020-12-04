from rpy2 import robjects
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, FORMATS
from pywps.app.Common import Metadata
from pywps.inout.formats import Format
from tempfile import NamedTemporaryFile

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger


class ClimdexSU(Process):
    """
    Takes a climdexInput object as input and computes the SU
    (summer days) climdexindex:  that is,  the annual count of days where
    daily maximum temperature exceeds 25 degreesCelsius
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
                "climdex_input",
                "climdexInput",
                abstract="Rdata (.rda) file containing R Object of type climdexInput",
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64")
                ],
            ),
            LiteralInput(
                "ci_name",
                "climdexInput name",
                abstract="Name of the climdexInput object",
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "output_path",
                "Output file name",
                abstract="Filename to store the count of days where tmax > 25 degC for each year (extension .rda)",
                data_type="string",
            ),
            LiteralInput(
                "su_name",
                "Summer days name",
                abstract="Name for the summer days output object",
                default="summer_days",
                min_occurs=0,
                max_occurs=1,
                data_type="string",
            ),
            log_level,
        ]

        outputs = [
            ComplexOutput(
                "summer_days_file",
                "Summer days output file",
                abstract="A vector containing the number of summer days for each year",
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64")
                ],
            ),
        ]

        super(ClimdexSU, self).__init__(
            self._handler,
            identifier="climdex_su",
            title="Climdex Summer Days",
            abstract="Computes the annual count of days where daily maximum temperature exceeds 25 degrees Celsius",
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
        climdex_input, ci_name, output_path, su_name, loglevel = [
            arg[0] for arg in collect_args(request, self.workdir).values()
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

        log_handler(
            self,
            response,
            "Processing Summer Days",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        # First load the climdexInput object into the environment
        robjects.r(f"load(file='{climdex_input}')")
        # Then assign that object a name in the python environment
        ci = robjects.r(ci_name)

        summer_days = climdex.climdex_su(ci)

        log_handler(
            self,
            response,
            "Saving summer days as R data file",
            logger,
            log_level=loglevel,
            process_step="build_rdata",
        )

        # Assign summer_days a name in the R environment
        robjects.r.assign(su_name, summer_days)
        robjects.r(f"save({su_name}, file='{output_path}')")

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )

        response.outputs["summer_days_file"].file = output_path

        # Clear R global env
        robjects.r("rm(list=ls())")

        log_handler(
            self,
            response,
            "Process Complete",
            logger,
            log_level=loglevel,
            process_step="complete",
        )

        return response
