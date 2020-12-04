from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, FORMATS, Format
from pywps.app.Common import Metadata
from rpy2 import robjects

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger


class ClimdexFD(Process):
    """
    Takes a climdexInput object as input and computes the FD
    (frost days) climdexindex:  that is,  the annual count of days when
    daily minimum temperature is below 0 degrees Celsius
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
                "ci_file",
                "climdexInput file",
                abstract="File that holds climdexInput object (recommended file extension .rda)",
                supported_formats=[
                    Format("application/rds", extension=".rds"),
                    Format("application/rda", extension=".rda"),
                ],
            ),
            LiteralInput(
                "ci_name",
                "climdexInput name",
                abstract="Name of the climdexInput obejct",
                min_occurs=0,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "output_file",
                "Output file name",
                abstract="Filename to store the output (recommended file extension .rda)",
                data_type="string",
            ),
            log_level,
        ]

        outputs = [
            ComplexOutput(
                "frost_days_file",
                "Frost days output file",
                abstract="A vector containing the number of frost days for each year",
                supported_formats=[Format("application/rds", extension=".rds")],
            ),
        ]

        super(ClimdexFD, self).__init__(
            self._handler,
            identifier="climdex_fd",
            title="Climdex Frost Days",
            abstract="Computes the annual count of days when daily minimum temperature is below 0 degrees Celsius",
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
        climdex_input, ci_name, output_file, loglevel = [
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

        log_handler(
            self,
            response,
            "Loading climdexInput from R data file",
            logger,
            log_level=loglevel,
            process_step="load_rdata",
        )

        robjects.r(f"load(file='{climdex_input}')")
        ci = robjects.r(ci_name)

        log_handler(
            self,
            response,
            "Processing Frost Days",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        climdex = get_package("climdex.pcic")
        frost_days = climdex.climdex_fd(ci)

        log_handler(
            self,
            response,
            "Saving frost days to R data file",
            logger,
            log_level=loglevel,
            process_step="build_rdata",
        )

        robjects.r.assign("frost_days", frost_days)
        robjects.r(f"save(frost_days, file='{output_file}')")

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )

        response.outputs["summer_days_file"].file = output_file

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
