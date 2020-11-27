from pywps import Process, LiteralInput, LiteralOutput
from pywps.app.Common import Metadata

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger


class ClimdexSU(Process):
    def __init__(self):
        self.status_percentage_steps = common_status_percentages

        inputs = [
            LiteralInput(
                "climdex_input",
                "climdexInput",
                abstract="R object Object of type climdexInput (file extension .rds)",
                data_type="string",
            ),
            log_level,
        ]

        outputs = [
            LiteralOutput(
                "summer_days_file",
                "Summer days output file",
                abstract="A vector containing the number of summer days for each year",
                data_type="string",
            ),
        ]

        super(ClimdexSU, self).__init__(
            self._handler,
            identifier="climdex_su",
            title="Climdex Summer Days",
            abstract="Computes the annual count of days where daily maximum temperature exceeds 25 degreesCelsius",
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
        climdex_input, loglevel = [input[0].data for input in request.inputs.values()]

        log_handler(
            self,
            response,
            "Starting Process",
            logger,
            log_level=loglevel,
            process_step="start",
        )
        climdex = get_package("climdex.pcic")

        # Get climdexIndex R oject from file
        base = get_package("base")
        with open(climdex_input):
            ci = base.readRDS(climdex_input)

        log_handler(
            self,
            response,
            "Processing Summer Days",
            logger,
            log_level=loglevel,
            process_step="process",
        )
        summer_days = climdex.climdex_su(ci)
        summer_days_dict = {
            base.names(summer_days)[index]: summer_days[index]
            for index in range(len(summer_days))
        }

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )

        response.outputs["summer_days_file"].data = summer_days_dict

        log_handler(
            self,
            response,
            "Process Complete",
            logger,
            log_level=loglevel,
            process_step="complete",
        )

        return response
