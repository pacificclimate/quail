from pywps import Process, ComplexInput, ComplexOutput, FORMATS, Format
from pywps.app.Common import Metadata

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger


class ClimdexFD(Process):
    """
    Takes a climdexInput object as input and computes the FD
    (frost days) climdexindex:  that is,  the annual count of days when
    daily minimum temperature is lower than 0 degrees Celsius
    """

    def __init__(self):
        self.status_percentage_steps = common_status_percentages

        inputs = [
            ComplexInput(
                "climdex_input",
                "climdexInput",
                abstract="R object Object of type climdexInput (file extension .rds)",
                supported_formats=[Format("application/rds", extension=".rds")],
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
            abstract="Computes the annual count of days when daily minimum temperature is lower than 0 degrees Celsius",
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
        climdex_input, loglevel = [
            arg[0] for arg in collect_args(request, self.workdir).values()
        ]

        base = get_package("base")
        with open(climdex_input):
            ci = base.load(file=request.inputs["climdex_input"][0].file)

        print(ci)

        return response
