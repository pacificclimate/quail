import sys, inspect, re, collections
from rpy2 import robjects
from pywps import Process, LiteralOutput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.R import get_package
from wps_tools.io import process_inputs_alpha
from quail.utils import logger, get_robj
from quail.io import avail_indices_inputs


class GetIndices(Process):
    """
    Takes a climdexInput object as input and returns a dictionary
    with the names of all the indices which may be computed as values
    and which processes they are accessible by as keys
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{"load_rdata": 10},
        )
        inputs = avail_indices_inputs
        outputs = [
            LiteralOutput(
                "avail_processes",
                "Available processes dictionary",
                abstract="Available climdex indices (values) and the processes to use to compute them (keys)",
                data_type="string",
            ),
        ]

        super(GetIndices, self).__init__(
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

    def available_processes(self, avail_indices):
        """
        Returns a dictionary containing the processes in quail (keys) which
        mention available indices (values) in their docstrings
        """
        processes = collections.defaultdict(list)
        indices = re.compile(r"climdex\.([a-zA-Z0-9]*)")

        for mod in [
            module
            for module in sys.modules
            if re.search("quail.processes.wps_*", module)
        ]:
            for name, class_ in inspect.getmembers(
                sys.modules[mod],
                lambda member: inspect.isclass(member) and member.__module__ == mod,
            ):
                [
                    processes[mod.split(".")[-1]].append(index)
                    for index in indices.findall(class_.__doc__)
                    if index in avail_indices
                ]

        return dict(processes)

    def _handler(self, request, response):
        ci_name, climdex_single_input, loglevel, output_file = process_inputs_alpha(request.inputs, avail_indices_inputs, self.workdir)

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
        ci = get_robj(climdex_single_input, ci_name)

        log_handler(
            self,
            response,
            "Processing climdex_get_available_indices",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        try:
            robjects.r.assign("ci", ci)
            avail_indices = climdex.climdex_get_available_indices(ci, False)
        except RRuntimeError as e:
            raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

        avail_processes = self.available_processes(avail_indices)

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )
        response.outputs["avail_processes"].data = avail_processes

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
