import os
from rpy2 import robjects
from pywps import Process, LiteralInput, LiteralOutput, ComplexOutput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import output_file, rda_output, vector_name


class ClimdexQuantile(Process):
    """
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
            LiteralInput(
                "data_file",
                "Data File",
                abstract="Path to the file containing data to compute quantiles on",
                min_occurs=1,
                max_occurs=0,
                data_type="string",
            ),
            LiteralInput(
                "data_vector",
                "Data Vector",
                abstract="Name of the R double vector data to compute quantiles on",
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "quantiles",
                "Quantiles",
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

    def _handler(self, request, response):
        data_file, data_vector, quantiles, output_file, vector_name, loglevel = [
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
        robjects.r("library(climdex.pcic)")

        log_handler(
            self,
            response,
            "Loading R data file",
            logger,
            log_level=loglevel,
            process_step="load_rdata",
        )
        data = load_rdata_to_python(data_file, data_vector)

        log_handler(
            self,
            response,
            f"Processing climdex.quantile",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        quantile_vector = robjects.r(f"climdex.quantile(data, {quantiles})")

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
        response.outputs["rda_output"].data = str(quantile_vector)

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
