from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.inout.formats import Format

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_path, rda_output


class ClimdexDays(Process):
    """
    Takes a climdexInput object as input and computes the annual count
    of days where daily maximum temperature satisfies some condition
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
                "days_type",
                "Day type to compute",
                abstract="Day type condition to compute: summer > 25 degC ; icing < 0 degC",
                allowed_values=["summer", "icing"],
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "vector_name",
                "Output vector variable name",
                abstract="Name to label the output vector",
                default="days",
                min_occurs=0,
                max_occurs=1,
                data_type="string",
            ),
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

        if days_type == "summer":
            return climdex.climdex_su(ci)
        elif days_type == "icing":
            return climdex.climdex_id(ci)

    def _handler(self, request, response):
        climdex_input, ci_name, output_path, days_type, vector_name, loglevel = [
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
        ci = load_rdata_to_python(climdex_input, ci_name)

        log_handler(
            self,
            response,
            f"Processing {days_type} Days",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        count_days = self.days(days_type, ci)

        log_handler(
            self,
            response,
            f"Saving {days_type} days as R data file",
            logger,
            log_level=loglevel,
            process_step="build_rdata",
        )

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
