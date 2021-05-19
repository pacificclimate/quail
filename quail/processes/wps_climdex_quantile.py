import os
from rpy2 import robjects
from pywps import Process, LiteralOutput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import rda_output, process_inputs_alpha
from wps_tools.R import (
    get_package,
    load_rdata_to_python,
    save_python_to_rdata,
    r_valid_name,
)
from quail.utils import logger, validate_vectors
from quail.io import quantile_inputs


class ClimdexQuantile(Process):
    """
    Wraps climdex.quantile
    This function implements R’s type=8 in a more efficient manner.
    """

    def __init__(self):
        self.status_percentage_steps = dict(
            common_status_percentages,
            **{
                "load_rdata": 10,
                "save_rdata": 90,
            },
        )
        inputs = quantile_inputs
        outputs = [
            LiteralOutput(
                "output_vector",
                "Output Vector",
                abstract="A vector of the quantiles in question",
                data_type="string",
            ),
            rda_output,
        ]

        super(ClimdexQuantile, self).__init__(
            self._handler,
            identifier="climdex_quantile",
            title="Climdex Quantile",
            abstract="Implements R’s type=8 in a more efficient manner",
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

    def unpack_data_file(self, data_file, data_vector):
        try:
            return load_rdata_to_python(data_file, data_vector)
        except (RRuntimeError, ProcessError, IndexError):
            pass

        try:
            return robjects.r(f"unlist(readRDS('{data_file}'))")
        except (RRuntimeError, ProcessError) as e:
            raise ProcessError(
                f"{type(e).__name__}: Data file must be a RDS file or "
                "a Rdata file containing an object of the given name"
            )

    def _handler(self, request, response):
        data_file, data_vector, loglevel, output_file, quantiles_vector, vector_name = process_inputs_alpha(request.inputs, quantile_inputs, self.workdir)
        validate_vectors([quantiles_vector])
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
            "Loading R data file",
            logger,
            log_level=loglevel,
            process_step="load_rdata",
        )

        if data_file:
            data = self.unpack_data_file(data_file, data_vector)
        else:
            data = robjects.r(data_vector)

        log_handler(
            self,
            response,
            "Processing climdex.quantile",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        try:
            quantiles = robjects.r(quantiles_vector)
            quantile_vector = climdex.climdex_quantile(data, quantiles)
        except RRuntimeError as e:
            raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

        log_handler(
            self,
            response,
            "Saving quantile as R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, quantile_vector, output_path)

        log_handler(
            self,
            response,
            "Building final output",
            logger,
            log_level=loglevel,
            process_step="build_output",
        )
        response.outputs["rda_output"].file = output_path
        response.outputs["output_vector"].data = str(quantile_vector)

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
