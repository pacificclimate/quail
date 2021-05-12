import os
from rpy2 import robjects
from pywps import Process
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError
from pywps.app.Common import Metadata

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, rda_output
from wps_tools.R import get_package
from quail.utils import logger, load_cis, process_inputs
from quail.io import dtr_inputs


class ClimdexDTR(Process):
    """
    Wraps climdex.dtr
    Computes the mean daily diurnal temperature range.
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "load_rdata": 10,
                "save_rdata": 90,
            },
        )
        inputs = dtr_inputs
        outputs = [rda_output]

        super(ClimdexDTR, self).__init__(
            self._handler,
            identifier="climdex_dtr",
            title="Climdex Mean Diurnal Temperature Range",
            abstract="Computes the mean daily diurnal temperature range.",
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
        climdex_input, freq, loglevel, output_file = process_inputs(request.inputs, dtr_inputs, self.workdir)

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
                f"Processing the mean daily diurnal temperature range {counter}/{total}",
                logger,
                log_level=loglevel,
                process_step="process",
            )

            for ci_name, ci in cis.items():
                try:
                    dtr = climdex.climdex_dtr(ci, freq)
                except RRuntimeError as e:
                    raise ProcessError(
                        msg=f"{type(e).__name__} for file {input}: {str(e)}"
                    )

                vector_name = f"dtr{counter}_{ci_name}"
                robjects.r.assign(vector_name, dtr)
                vectors.append(vector_name)
            counter += 1

        log_handler(
            self,
            response,
            "Saving dtr vectors to Rdata file",
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
