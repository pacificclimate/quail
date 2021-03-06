import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError
from pywps.app.Common import Metadata

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, rda_output
from wps_tools.R import get_package
from quail.utils import logger, load_cis, collect_literal_inputs
from quail.io import climdex_input, output_file


class ClimdexRMM(Process):
    """
    wraps climdex.r10mm, climdex.r20mm and climdex.rnnmm
    The annual count of days where daily precipitation is more
    than [threshold] mm per day
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
                abstract="mm threshold for daily precipitation",
                min_occurs=1,
                max_occurs=1,
                data_type="float",
            ),
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexRMM, self).__init__(
            self._handler,
            identifier="climdex_rmm",
            title="Climdex RMM",
            abstract="The annual count of days where daily precipitation is more than [threshold] mm per day",
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

    def threshold_func(self, threshold, ci):
        climdex = get_package("climdex.pcic")

        if threshold == 10.0:
            return climdex.climdex_r10mm(ci)
        if threshold == 20.0:
            return climdex.climdex_r20mm(ci)
        else:
            return climdex.climdex_rnnmm(ci, threshold)

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
        climdex = get_package("climdex.pcic")
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
                f"Processing the annual count of days where daily precipitation is more than {threshold}mm per day for file {i}",
                logger,
                log_level=loglevel,
                process_step="process",
            )

            for ci_name, ci in cis.items():
                try:
                    robjects.r.assign("ci", ci)
                    count_days = self.threshold_func(threshold, ci)
                except RRuntimeError as e:
                    raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

                vector_name = f"r{threshold}mm{i}_{ci_name}"
                robjects.r.assign(vector_name, count_days)
                vectors.append(vector_name)

        log_handler(
            self,
            response,
            f"Saving climdex.r{threshold}mm outputs to R data file",
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
