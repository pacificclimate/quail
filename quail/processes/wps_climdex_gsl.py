import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError


from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, collect_args, rda_output, vector_name
from wps_tools.R import get_package, save_python_to_rdata, r_valid_name
from quail.utils import logger, load_ci, collect_literal_inputs
from quail.io import ci_rda, ci_rds, ci_name, output_file


class ClimdexGSL(Process):
    """
    Wraps climdex.gsl
    Computes the growing season length (GSL): Growing season length
    is the number of days between the start of the first spell of warm days
    in the first half of the year, defined as six or more days with mean
    temperature above 5 degrees Celsius, and the start of the first spell
    of cold days in the second half of the year, defined as six or more days
    with a mean temperature below 5 degrees Celsius
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
            ci_rda,
            ci_rds,
            ci_name,
            output_file,
            vector_name,
            LiteralInput(
                "gsl_mode",
                "GSL mode",
                abstract="Growing season length method to use. The three alternate modes provided ('GSL_first', 'GSL_max', and 'GSL_sum') are for testing purposes only.",
                default="GSL",
                min_occurs=0,
                max_occurs=1,
                allowed_values=["GSL", "GSL_first", "GSL_max", "GSL_sum"],
                data_type="string",
            ),
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexGSL, self).__init__(
            self._handler,
            identifier="climdex_gsl",
            title="Climdex Growing Seasonal Length",
            abstract="Computes the growing season length (GSL)",
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
        (
            ci_name,
            output_file,
            vector_name,
            gsl_mode,
            loglevel,
        ) = collect_literal_inputs(request)
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
        args = collect_args(request, self.workdir)
        ci = load_ci(args, ci_name)

        log_handler(
            self,
            response,
            "Processing growing seasonal length",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        try:
            gsl = climdex.climdex_gsl(ci, gsl_mode)
        except RRuntimeError as e:
            raise ProcessError(msg=f"{type(e).__name__}: {str(e)}")

        log_handler(
            self,
            response,
            "Saving gsl as R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, gsl, output_path)

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
