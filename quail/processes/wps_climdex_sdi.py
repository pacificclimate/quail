import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_file, rda_output, vector_name


class ClimdexSDI(Process):
    """
    Cold or warm spell duration index

    The warm spell duration index is defined as the number
    of days each year which are part of a "warmspell". A
    "warm spell" is defined as a sequence of 6 or more days
    in which the daily maximumtemperature exceeds the 90th
    percentile of daily maximum temperature for a 5-day
    running windowsurrounding this day during the baseline
    period.
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
            LiteralInput(
                "func",
                "Function to compute",
                abstract="Compute climdex.wsdi (Warm spell duration index)",
                allowed_values=["wsdi"],
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "span_years",
                "Spells can span years",
                abstract="Specifies whether spells can cross year boundaries",
                default=False,
                data_type="boolean"
            ),
            vector_name,
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexSDI, self).__init__(
            self._handler,
            identifier="climdex_sdi",
            title="Climdex SDI",
            abstract="Cold or warm spell duration index",
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
        climdex_input, ci_name, output_file, func, span_years, vector_name, loglevel = [
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
        climdex = get_package("climdex.pcic")

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
            f"Processing climdex.{func} for each year",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        if span_years:
            spells = robjects.r(f"climdex.{func}(ci, T)")
        else:
            spells = robjects.r(f"climdex.{func}(ci)")

        log_handler(
            self,
            response,
            f"Saving {func} for each year to R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, spells, output_path)

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
