import os
from rpy2 import robjects
from pywps import Process, LiteralInput, LiteralOutput, ComplexInput, Format
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, collect_args, rda_output, vector_name
from wps_tools.R import get_package, load_rdata_to_python, save_python_to_rdata
from quail.utils import logger, collect_literal_inputs, load_rda, r_valid_name
from quail.io import output_file


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
        inputs = [
            ComplexInput(
                "data_file",
                "Data File",
                abstract="Path to the file containing data to compute quantiles on",
                min_occurs=0,
                max_occurs=1,
                supported_formats=[
                    Format("application/x-gzip", extension=".rda", encoding="base64")
                ],
            ),
            LiteralInput(
                "data_vector",
                "Data Vector",
                abstract="R double vector data to compute quantiles on",
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "quantiles_vector",
                "Quantiles_vector",
                abstract="Quantiles to be computed",
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            output_file,
            vector_name,
            log_level,
        ]

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

    def collect_args_wrapper(self, request):
        literal_inputs = collect_literal_inputs(request)
        if "data_file" in collect_args(request, self.workdir).keys():
            data_file = collect_args(request, self.workdir)["data_file"][0]
        else:
            data_file = None

        return [data_file] + literal_inputs

    def _handler(self, request, response):
        (
            data_file,
            data_vector,
            quantiles_vector,
            output_file,
            vector_name,
            loglevel,
        ) = self.collect_args_wrapper(request)
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
            data = load_rda(data_file, data_vector)
        else:
            data = robjects.r(data_vector)

        log_handler(
            self,
            response,
            f"Processing climdex.quantile",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        try:
            quantiles = robjects.r(quantiles_vector)
            quantile_vector = climdex.climdex_quantile(data, quantiles)
        except RRuntimeError as e:
            raise ProcessError(msg=str(e))

        log_handler(
            self,
            response,
            f"Saving quantile as R data file",
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
