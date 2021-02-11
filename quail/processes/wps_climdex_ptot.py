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


class ClimdexPtot(Process):
    """
    Wraps climdex.r95ptot, climdex.r99ptot and climdex.prcptot
    Computes the annual sum of precipitation in days where daily precipitation
    exceeds the daily precipitation threshold in the base period.
    If threshold is not given, annual sum of precipitation in wet days (> 1mm)
    will be calculated.
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
                "threshold",
                "Threshold",
                abstract="Daily precipitation threshold",
                allowed_values=[0, 95, 99],
                default=0,
                min_occurs=0,
                max_occurs=1,
                data_type="integer",
            ),
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexPtot, self).__init__(
            self._handler,
            identifier="climdex_ptot",
            title="Climdex Temperature Percentiles",
            abstract="Total daily precipitation exceeding threshold",
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

    def get_func(self, threshold):
        if threshold == 0:
            return "prc"
        else:
            return f"r{threshold}"

    def _handler(self, request, response):
        output_file, threshold, loglevel = collect_literal_inputs(request)
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
        func = self.get_func(threshold)
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
                f"Processing climdex.{func}ptot for file {i}",
                logger,
                log_level=loglevel,
                process_step="process",
            )

            for ci_name, ci in cis.items():
                try:
                    robjects.r.assign("ci", ci)
                    mothly_pct = robjects.r(f"climdex.{func}ptot(ci)")
                except RRuntimeError as e:
                    raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

                vector_name = f"{func}{i}_{ci_name}"
                robjects.r.assign(vector_name, mothly_pct)
                vectors.append(vector_name)

        log_handler(
            self,
            response,
            f"Saving {func}ptot vectors to Rdata file",
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
