from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.inout.formats import Format

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_path, rda_output


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
            climdex_input,
            ci_name,
            output_path,
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

        outputs = [rda_output]

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

        ci = load_rdata_to_python(climdex_input, ci_name)
        summer_days = climdex.climdex_su(ci)

        log_handler(
            self,
            response,
            "Saving summer days as R data file",
            logger,
            log_level=loglevel,
            process_step="build_rdata",
        )

        save_python_to_rdata(su_name, summer_days, output_path)

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )

        response.outputs["rda_output"].file = output_path

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
