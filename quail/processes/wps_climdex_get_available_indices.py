import os, sys, inspect, re, collections
from rpy2 import robjects
from pywps import Process, LiteralInput, LiteralOutput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_file, vector_name, rda_output


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
        inputs = [
            climdex_input,
            ci_name,
            output_file,
            vector_name,
            log_level,
        ]

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
        indices = re.compile("climdex\.([a-zA-Z0-9]*)")

        for mod in [
            module for module in sys.modules if re.search("quail.processes.wps_*", module)
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
        (
            climdex_input,
            ci_name,
            output_file,
            vector_name,
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

        avail_indices = climdex.climdex_get_available_indices(ci, False)
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
