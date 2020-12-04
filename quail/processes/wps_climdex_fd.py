import os
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, FORMATS, Format
from pywps.app.Common import Metadata
from rpy2 import robjects
from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, load_rdata, save_rdata, logger
from quail.io import ci_file, ci_name, output_obj, output_file


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
        inputs = [ci_file, ci_name, output_obj, output_file, log_level]

        outputs = [
            ComplexOutput(
                "frost_days_file",
                "Frost days output file",
                abstract="A vector containing the number of frost days for each year",
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64")
                ],
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
        climdex_input, ci_name, output_obj, output_file, loglevel = [
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

        ci = load_rdata(climdex_input, ci_name)

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
            process_step="save_rdata",
        )

        output_path = os.path.join(self.workdir, output_file)
        save_rdata(output_obj, frost_days, output_path)

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )

        response.outputs["frost_days_file"].file = output_path

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
