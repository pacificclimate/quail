import os
from rpy2 import robjects
from pywps import Process
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import rda_output, process_inputs_alpha
from wps_tools.R import get_package
from quail.utils import logger, load_cis
from quail.io import rxnday_inputs


class ClimdexRxnday(Process):
    """
    Wraps
    climdex.rx1day: monthly or annual maximum 1-day precipitation
    climdex.rx5day: monthly or annual maximum 5-day consecutive precipitation.
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "load_rdata": 10,
                "save_rdata": 90,
            },
        )
        inputs = rxnday_inputs
        outputs = [rda_output]

        super(ClimdexRxnday, self).__init__(
            self._handler,
            identifier="climdex_rxnday",
            title="Climdex Monthly Maximum n (1 or 5) day Precipitation",
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

    def rxnday_func(self, ci, num_days, freq, center_mean_on_last_day):
        climdex = get_package("climdex.pcic")

        if num_days == 1:
            return climdex.climdex_rx1day(ci, freq)

        elif num_days == 5:
            return climdex.climdex_rx5day(ci, freq, center_mean_on_last_day)

    def _handler(self, request, response):
        (
            center_mean_on_last_day,
            climdex_input,
            freq,
            loglevel,
            num_days,
            output_file,
        ) = process_inputs_alpha(request.inputs, rxnday_inputs, self.workdir)

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
                f"Processing Monthly Maximum {num_days}-day Precipitation for file {counter}/{total}",
                logger,
                log_level=loglevel,
                process_step="process",
            )

            for ci_name, ci in cis.items():
                try:
                    robjects.r.assign("ci", ci)
                    rxnday = self.rxnday_func(
                        ci, num_days, freq, center_mean_on_last_day
                    )
                except RRuntimeError as e:
                    raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

                vector_name = f"rx{num_days}day{counter}_{ci_name}"
                robjects.r.assign(vector_name, rxnday)
                vectors.append(vector_name)
            counter += 1

        log_handler(
            self,
            response,
            f"Saving rx{num_days}day vector to R data file",
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
