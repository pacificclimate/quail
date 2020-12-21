import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_file, rda_output, vector_name, freq


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
        inputs = [
            climdex_input,
            ci_name,
            output_file,
            vector_name,
            freq,
            LiteralInput(
                "num_days",
                "Number of days of precipitation",
                abstract="Compute rx[1]day or rx[5]day",
                allowed_values=[1, 5],
                data_type="positiveInteger",
            ),
            LiteralInput(
                "center_mean_on_last_day",
                "Center mean on last day",
                abstract="Whether to center the 5-day running mean on the last day of the window, insteadof the center day.",
                min_occurs=0,
                max_occurs=1,
                default=False,
                data_type="boolean",
            ),
            log_level,
        ]

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
            climdex_input,
            ci_name,
            output_file,
            vector_name,
            freq,
            num_days,
            center_mean_on_last_day,
            loglevel,
        ) = [arg[0] for arg in collect_args(request, self.workdir).values()]

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
            f"Processing Monthly Maximum {num_days}-day Precipitation",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        rxnday = self.rxnday_func(ci, num_days, freq, center_mean_on_last_day)

        log_handler(
            self,
            response,
            f"Saving rx{num_days}day vector to R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, rxnday, output_path)

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
