import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, rda_output
from quail.utils import logger, load_cis, collect_literal_inputs
from quail.io import climdex_input, output_file


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
        inputs = [
            climdex_input,
            output_file,
            LiteralInput(
                "func",
                "Function to compute",
                abstract="Compute climdex.wsdi (Warm spell duration index)",
                allowed_values=["wsdi", "csdi", "cdd", "cwd"],
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "span_years",
                "Spells can span years",
                abstract="Specifies whether spells can cross year boundaries",
                default=False,
                data_type="boolean",
            ),
            log_level,
        ]

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
        (
            output_file,
            func,
            span_years,
            loglevel,
        ) = collect_literal_inputs(request)
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
                f"Loading climdexInput from R data file {i}",
                logger,
                log_level=loglevel,
                process_step="load_rdata",
            )
            cis = load_cis(climdex_input[i].file)

            log_handler(
                self,
                response,
                f"Processing climdex.{func} for each year for file {i}",
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

                vector_name = f"{func}{i}_{ci_name}"
                robjects.r.assign(vector_name, spells)
                vectors.append(vector_name)

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
