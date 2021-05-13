import os
from rpy2 import robjects
from pywps import Process
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import rda_output
from quail.utils import logger, load_cis, process_inputs
from quail.io import spells_inputs


class ClimdexSpells(Process):
    """
    Cold or warm spell duration index and maximum consecutive dry or wet days
    Wraps
    - climdex.cdd
    - climdex.csdi
    - climdex.cwd
    - climdex.wsdi
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "load_rdata": 10,
                "save_rdata": 90,
            },
        )
        inputs = spells_inputs
        outputs = [rda_output]

        super(ClimdexSpells, self).__init__(
            self._handler,
            identifier="climdex_spells",
            title="Climdex Spells",
            abstract="Cold (csdi) or warm (wsdi) spell duration index and maximum consecutive dry (cdd) or wet (cwd) days",
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
        climdex_input, func, loglevel, output_file, span_years = process_inputs(request.inputs, spells_inputs, self.workdir)

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

        counter = 1
        total = len(climdex_input)

        for input in climdex_input:
            log_handler(
                self,
                response,
                f"Loading climdexInput from R data file {counter}/{total}",
                logger,
                log_level=loglevel,
                process_step="load_rdata",
            )
            cis = load_cis(input)

            log_handler(
                self,
                response,
                f"Processing climdex.{func} for each year for file {counter}/{total}",
                logger,
                log_level=loglevel,
                process_step="process",
            )

            for ci_name, ci in cis.items():
                try:
                    robjects.r.assign("ci", ci)
                    robjects.r.assign("span_years", span_years)
                    spells = robjects.r(f"climdex.{func}(ci, span_years)")
                except RRuntimeError as e:
                    raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

                vector_name = f"{func}{counter}_{ci_name}"
                robjects.r.assign(vector_name, spells)
                vectors.append(vector_name)
            counter += 1

        log_handler(
            self,
            response,
            f"Saving {func} outputs to R data file",
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
