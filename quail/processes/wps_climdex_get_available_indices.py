import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name

class ClimdexGetAvailableIndices(Process):
    """
    Takes a climdexInput object as input and returns the names of all the
    indices which may be computed or, if get_function_names is True (the
    default), the names of the functions corresponding to the indices
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{"load_rdata": 10},
        )
        inputs = [
            climdex_input,
            ci_name,
            LiteralInput(
                "get_function_names",
                "Get function names",
                abstract="Whether to return function names",
                default=True,
                min_occurs=0,
                max_occurs=1,
                data_type="boolean",
            ),
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexGetAvailableIndices, self).__init__(
            self._handler,
            identifier="climdex_get_available_indices",
            title="Climdex Get Available Indices",
            abstract="Returns the names of all the indices which may be computed or, if get_function_names is TRUE, the names of the functions corresponding to the indices.",
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

    processes = {
        "su": "wps_climdex_days",
        "id": "wps_climdex_days",
        "txx":"wps_climdex_mmdmt",
        "txn": "wps_climdex_mmdmt",
        "tx10p":"wps_climdex_temp_pctl",
        "tx90p":"wps_climdex_temp_pctl",
        "wsdi":"wps_climdex_spells",
        "fd":"wps_climdex_days",
        "tr":"", "tnx":"wps_climdex_mmdmt",
        "tnn":"wps_climdex_mmdmt",
        "tn10p":"",
        "tn90p":"wps_climdex_temp_pctl",
        "csdi":"",
        "rx1day":"",
        "rx5day":"",
        "sdii":"",
        "r10mm":"wps_climdex_rmm",
        "r20mm":"wps_climdex_rmm",
        "rnnmm":"wps_climdex_rmm",
        "cdd":"wps_climdex_spells",
        "cwd":"wps_climdex_spells",
        "r95ptot":"",
        "r99ptot":"",
        "prcptot":"",
        "gsl":"wps_climdex_gsl",
        "dtr":""
    }

    def _handler(self, request, response):
        climdex_input, ci_name, get_function_names, loglevel = [
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
            f"Processing climdex_get_available_indices",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        indices = climdex_get_available_indices(ci, get_function_names)

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
