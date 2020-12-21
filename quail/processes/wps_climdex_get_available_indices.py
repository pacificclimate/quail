import os, sys, inspect, re
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
    Takes a climdexInput object as input and returns the names of all the
    indices which may be computed or, if get_function_names is True (the
    default), the names of the functions corresponding to the indices
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

        outputs = [
            rda_output,
            LiteralOutput(
                "avail_processes",
                "Available processes dictionary",
                abstract="Available climdex indices (keys) and the processes to use to compute them (values)",
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

    def available_processes(self):
        processes = {}
        for mod in sys.modules:
            if re.search("quail.processes.*", mod):
                classes = inspect.getmembers(
                    sys.modules[mod],
                    lambda member: inspect.isclass(member) and member.__module__ == mod,
                )
                for name, class_ in classes:
                    indices = re.compile('climdex\.([a-zA-Z0-9]*)')
                    processes[mod.split(".")[-1]] = indices.findall(class_.__doc__)

        return processes

    def _handler(self, request, response):
        (
            climdex_input,
            ci_name,
            output_file,
            vector_name,
            get_function_names,
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

        indices = climdex.climdex_get_available_indices(ci, get_function_names)

        avail_processes = {
            index.split(".")[-1]: self.processes[index.split(".")[-1]]
            for index in indices
        }

        log_handler(
            self,
            response,
            "Saving indices to R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, indices, output_path)

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )
        response.outputs["rda_output"].file = output_path
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
