import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_file, rda_output, vector_name


class ClimdexGSL(Process):
    """
    Computes the growing season length (GSL): Growing season length
    is the number of days between the startof the first spell of warm days
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
            climdex_input,
            ci_name,
            output_file,
            vector_name,
            LiteralInput(
                "gsl_mode",
                "GSL mode",
                abstract="Growing season length method to use. The three alternate modes provided ('GSL_first', 'GSL_max', and 'GSL_sum') are for testing pur-poses only.",
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
        climdex_input, ci_name, output_file, vector_name, gsl_mode, loglevel = [
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
            "Processing growing seasonal length",
            logger,
            log_level=loglevel,
            process_step="process",
        )
        climdex = get_package("climdex.pcic")
        gsl = climdex.climdex_gsl(ci, gsl_mode)

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