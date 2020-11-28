from pywps import Process, LiteralInput, ComplexOutput, FORMATS
from pywps.app.Common import Metadata
import json

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
                "build_json": 90,
            },
        )

        inputs = [
            LiteralInput(
                "climdex_input",
                "climdexInput",
                abstract="R object Object of type climdexInput (file extension .rds)",
                data_type="string",
            ),
            LiteralInput(
                "output_path",
                "Output file name",
                abstract="Filename to store the count of days where tmax > 25 degC for each year",
                data_type="string",
            ),
            log_level,
        ]

        outputs = [
            ComplexOutput(
                "summer_days_file",
                "Summer days output file",
                abstract="A vector containing the number of summer days for each year",
                supported_formats=[FORMATS.JSON],
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
        climdex_input, output_path, loglevel = [
            input[0].data for input in request.inputs.values()
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

        log_handler(
            self,
            response,
            "Saving summer days to json",
            logger,
            log_level=loglevel,
            process_step="build_json",
        )
        with open(output_path, "w") as json_file:
            json.dump(
                {
                    base.names(summer_days)[index]: summer_days[index]
                    for index in range(len(summer_days))
                },
                json_file,
            )

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )

        response.outputs["summer_days_file"].file = output_path

        log_handler(
            self,
            response,
            "Process Complete",
            logger,
            log_level=loglevel,
            process_step="complete",
        )

        return response
