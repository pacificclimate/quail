import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError

from wps_tools.logging import log_handler, common_status_percentages
from wps_tools.io import log_level, collect_args, rda_output, vector_name
from wps_tools.R import get_package, load_rdata_to_python, save_python_to_rdata
from quail.utils import logger, load_ci, r_valid_name
from quail.io import climdex_input, ci_name, output_file


class ClimdexSDII(Process):
    """
    Wraps climdex.sdii
    Computes the climdex index SDII, or Simple Precipitation Intensity Index.
    This is defined as the sum of precipitation in wet days (days with
    preciptitation over 1mm) during the year divided by the number of wet days
    in the year.
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
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexSDII, self).__init__(
            self._handler,
            identifier="climdex_sdii",
            title="Climdex Simple Precipitation Intensity Index",
            abstract="Defined as the sum of precipitation in wet days (days with preciptitation over 1mm) during the year divided by the number of wet days in the year.",
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
        climdex_input, ci_name, output_file, vector_name, loglevel = [
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
            "Processing the mean daily diurnal temperature range",
            logger,
            log_level=loglevel,
            process_step="process",
        )

        try:
            sdii = climdex.climdex_sdii(ci)
        except RRuntimeError as e:
            raise ProcessError(msg=str(e))

        log_handler(
            self,
            response,
            "Saving dtr vector to R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, sdii, output_path)

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
