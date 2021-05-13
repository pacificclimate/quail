import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError


from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import rda_output
from wps_tools.R import get_package
from quail.utils import logger, load_cis, process_inputs
from quail.io import gsl_inputs


class ClimdexGSL(Process):
    """
    Wraps climdex.gsl
    Computes the growing season length (GSL): Growing season length
    is the number of days between the start of the first spell of warm days
    in the first half of the year, defined as six or more days with mean
    temperature above 5 degrees Celsius, and the start of the first spell
    of cold days in the second half of the year, defined as six or more days
    with a mean temperature below 5 degrees Celsius
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "load_rdata": 10,
                "save_rdata": 90,
            },
        )

        inputs = gsl_inputs
        outputs = [rda_output]

        super(ClimdexGSL, self).__init__(
            self._handler,
            identifier="climdex_gsl",
            title="Climdex Growing Seasonal Length",
            abstract="Computes the growing season length (GSL)",
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
        climdex_input, gsl_mode, loglevel, output_file = process_inputs(request.inputs, gsl_inputs, self.workdir)

        log_handler(
            self,
            response,
            "Starting Process",
            logger,
            log_level=loglevel,
            process_step="start",
        )
        climdex = get_package("climdex.pcic")
        vectors = []

        counter = 1
        total = len(climdex_input)

        for input in climdex_input:
            log_handler(
                self,
                response,
                f"Loading climdexInputs from R data file {counter}/{total}",
                logger,
                log_level=loglevel,
                process_step="load_rdata",
            )
            cis = load_cis(input)

            log_handler(
                self,
                response,
                f"Processing growing seasonal length for file {counter}/{total}",
                logger,
                log_level=loglevel,
                process_step="process",
            )

            for ci_name, ci in cis.items():
                try:
                    robjects.r.assign("ci", ci)
                    gsl = climdex.climdex_gsl(ci, gsl_mode)
                except RRuntimeError as e:
                    raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

                vector_name = f"gsl{counter}_{ci_name}"
                robjects.r.assign(vector_name, gsl)
                vectors.append(vector_name)
            counter += 1

        log_handler(
            self,
            response,
            "Saving gsl vectors to R data file",
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
