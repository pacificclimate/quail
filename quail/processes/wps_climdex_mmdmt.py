import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, collect_args, rda_output, vector_name
from wps_tools.R import (
    get_package,
    load_rdata_to_python,
    save_python_to_rdata,
    r_valid_name,
)
from quail.utils import logger, load_ci
from quail.io import climdex_input, ci_name, output_file, freq


class ClimdexMMDMT(Process):
    """
    This process wraps climdex functions
    - climdex.txx: Monthly (or annual) Maximum of Daily Maximum Temperature
    - climdex.tnx: Monthly (or annual) Maximum of Daily Minimum Temperature
    - climdex.txn: Monthly (or annual) Minimum of Daily Maximum Temperature
    - climdex.tnn: Monthly (or annual) Minimum of Daily Minimum Temperature
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
                "month_type",
                "Month type to compute",
                abstract="Min/ max daily temperature type to compute",
                allowed_values=["txx", "tnx", "txn", "tnn"],
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            freq,
            vector_name,
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexMMDMT, self).__init__(
            self._handler,
            identifier="climdex_mmdmt",
            title="Climdex MMDMT",
            abstract=""" climdex_mmdmt includes the functions:
                - climdex.txx: Monthly (or annual) Maximum of Daily Maximum Temperature
                - climdex.tnx: Monthly (or annual) Maximum of Daily Minimum Temperature
                - climdex.txn: Monthly (or annual) Minimum of Daily Maximum Temperature
                - climdex.tnn: Monthly (or annual) Minimum of Daily Minimum Temperature
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
        climdex_input, ci_name, output_file, month_type, freq, vector_name, loglevel = [
            arg[0] for arg in collect_args(request, self.workdir).values()
        ]
        r_valid_name(vector_name)

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
        ci = load_ci(climdex_input, ci_name)

        log_handler(
            self,
            response,
            f"Processing {month_type}",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        try:
            temps = robjects.r(f"climdex.{month_type}(ci, freq='{freq}')")
        except RRuntimeError as e:
            raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

        log_handler(
            self,
            response,
            f"Saving {month_type} vector to R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, temps, output_path)

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
