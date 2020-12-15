import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.exceptions import ProcessError
from pywps.app.Common import Metadata

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_file, rda_output, vector_name


class ClimdexRMM(Process):
    """
    The annual count of days where daily precipitation is more
    than [threshold] mm per day
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
            LiteralInput(
                "threshold",
                "Threshold",
                abstract="mm threshold for daily precipitation",
                min_occurs=1,
                max_occurs=1,
                data_type="float",
            ),
            vector_name,
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexRMM, self).__init__(
            self._handler,
            identifier="climdex_rmm",
            title="Climdex RMM",
            abstract="The annual count of days where daily precipitation is more than [threshold] mm per day",
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

    def threshold_func(self, threshold, ci):
        climdex = get_package("climdex.pcic")

        if threshold == 10.0:
            return climdex.climdex_r10mm(ci)
        if threshold == 20.0:
            return climdex.climdex_r20mm(ci)
        else:
            return climdex.climdex_rnnmm(ci, threshold)

    def _handler(self, request, response):
        climdex_input, ci_name, output_file, threshold, vector_name, loglevel = [
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
            f"Processing the annual count of days where daily precipitation is more than {threshold}mm per day",
            logger,
            log_level=loglevel,
            process_step="process",
        )
        count_days = self.threshold_func(threshold, ci)

        log_handler(
            self,
            response,
            f"Saving climdex.r{threshold}mm output as R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, threshold, output_path)

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