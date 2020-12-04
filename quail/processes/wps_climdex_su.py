import os
from rpy2 import robjects
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, FORMATS
from pywps.app.Common import Metadata
from pywps.inout.formats import Format
from tempfile import NamedTemporaryFile

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, load_rdata, save_rdata, logger
from quail.io import ci_file, ci_name, output_obj, output_file


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
        inputs = [ci_file, ci_name, output_obj, output_file, log_level]

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
        climdex_input, ci_name, su_name, output_file, loglevel = [
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

        ci = load_rdata(climdex_input, ci_name)
        summer_days = climdex.climdex_su(ci)

        log_handler(
            self,
            response,
            "Saving summer days as R data file",
            logger,
            log_level=loglevel,
            process_step="build_rdata",
        )

        output_path = os.path.join(self.workdir, output_file)
        save_rdata(su_name, summer_days, output_path)

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
