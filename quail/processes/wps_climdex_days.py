import os
from rpy2 import robjects
from rpy2.rinterface_lib.embedded import RRuntimeError
from pywps import Process, LiteralInput
from pywps.app.exceptions import ProcessError
from pywps.app.Common import Metadata

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, rda_output
from quail.utils import logger, load_cis, collect_literal_inputs
from quail.io import climdex_input, output_file


class ClimdexDays(Process):
    """
    Takes a climdexInput object as input and computes the annual count
    of days where daily temperature satisfies some condition.
    - climdex.su "summer": the annual count of days where daily maximum temperature
    exceeds 25 degrees Celsius
    - climdex.id "icing": the annual count of days where daily maximum temperature
    was below 0 degrees Celsius
    - climdex.fd "frost": the annual count of days where daily minimum temperature
    was below 0 degrees Celsius
    - climdex.tr "tropical nights": the annual count of days where daily minimum
    temperature stays above 20 degrees Celsius
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "prep_ci": 10,
                "save_rdata": 90,
            },
        )
        inputs = [
            climdex_input,
            output_file,
            LiteralInput(
                "days_type",
                "Day type to compute",
                abstract="Day type condition to compute",
                allowed_values=["su", "id", "fd", "tr"],
                min_occurs=1,
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
            abstract="""
                Takes a climdexInput object as input and computes the annual count of days where daily temperature satisfies some condition.
                "summer": the annual count of days where daily maximum temperature
                exceeds 25 degreesCelsius
                "icing": the annual count of days where daily maximum temperature
                was below 0 degrees Celsius
                "frost": the annual count of days where daily minimum temperature
                was below 0 degrees Celsius
                "tropical nights": the annual count of days where daily minimum
                temperature stays above 20 degrees Celsius
            """,
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
        output_file, days_type, loglevel = collect_literal_inputs(request)
        climdex_input = request.inputs["climdex_input"]

        log_handler(
            self,
            response,
            "Starting Process",
            logger,
            log_level=loglevel,
            process_step="start",
        )
        robjects.r("library(climdex.pcic)")
        vectors = []

        for i in range(len(climdex_input)):
            log_handler(
                self,
                response,
                f"Preparing climdexInputs {i}",
                logger,
                log_level=loglevel,
                process_step="prep_ci",
            )
            cis = load_cis(climdex_input[i].file)

            log_handler(
                self,
                response,
                f"Processing {days_type} count {i}",
                logger,
                log_level=loglevel,
                process_step="process",
            )

            for ci_name, ci in cis.items():
                try:
                    robjects.r.assign("ci", ci)
                    count_days = robjects.r(f"climdex.{days_type}(ci)")
                except RRuntimeError as e:
                    raise ProcessError(msg=f"{type(e).__name__} in file {i}: {str(e)}")

                vector_name = f"{days_type}{i}_{ci_name}"
                robjects.r.assign(vector_name, count_days)
                vectors.append(vector_name)

        log_handler(
            self,
            response,
            f"Saving {days_type} counts to R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        robjects.r["save"](*vectors, file=output_path)

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
