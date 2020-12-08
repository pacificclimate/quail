import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_file, rda_output, vector_name


class ClimdexDays(Process):
    """
    Takes a climdexInput object as input and computes the annual count
    of days where daily temperature satisfies some condition.
    - "summer": the annual count of days where daily maximum temperature
    exceeds 25 degreesCelsius
    - "icing": the annual count of days where daily maximum temperature
    was below 0 degrees Celsius
    - "frost": the annual count of days where daily minimum temperature
    was below 0 degrees Celsius
    - "tropical nights": the annual count of days where daily minimum
    temperature stays above 20 degrees Celsius
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
            climdex_input,
            ci_name,
            output_file,
            LiteralInput(
                "days_type",
                "Day type to compute",
                abstract="Day type condition to compute",
                allowed_values=[
                    "summer days",
                    "icing days",
                    "frost days",
                    "tropical nights",
                ],
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            vector_name,
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexDays, self).__init__(
            self._handler,
            identifier="climdex_days",
            title="Climdex Days",
            abstract="Computes the annual count of days where daily maximum temperature satisfies some condition",
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

    def days(self, days_type, ci):
        climdex = get_package("climdex.pcic")

        if days_type == "summer days":
            return climdex.climdex_su(ci)
        elif days_type == "icing days":
            return climdex.climdex_id(ci)
        elif days_type == "frost days":
            return climdex.climdex_fd(ci)
        elif days_type == "tropical nights":
            return climdex.climdex_tr(ci)
        else:
            raise ValueError("invalid days_type")

    def _handler(self, request, response):
        climdex_input, ci_name, output_file, days_type, vector_name, loglevel = [
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
        ci = load_rdata_to_python(climdex_input, ci_name)

        log_handler(
            self,
            response,
            f"Processing {days_type} count",
            logger,
            log_level=loglevel,
            process_step="process",
        )
        count_days = self.days(days_type, ci)

        log_handler(
            self,
            response,
            f"Saving {days_type} count as R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, count_days, output_path)

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
