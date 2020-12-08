import os
from rpy2 import robjects
from pywps import Process, LiteralInput
from pywps.app.Common import Metadata

from wps_tools.utils import log_handler, collect_args, common_status_percentages
from wps_tools.io import log_level
from quail.utils import get_package, logger, load_rdata_to_python, save_python_to_rdata
from quail.io import climdex_input, ci_name, output_file, rda_output, vector_name


class ClimdexMMDMT(Process):
    """
    This process wraps climdex function
    - climdex.txx: Monthly (or annual) Maximum of Daily Maximum Temperature
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
                "month_type",
                "Month type to compute",
                abstract="Min/ max daily temperature type to compute",
                allowed_values=["txx"],
                min_occurs=1,
                max_occurs=1,
                data_type="string",
            ),
            LiteralInput(
                "freq",
                "Frequency",
                abstract="Time frequency to aggregate to",
                allowed_values=["monthly", "annual"],
                default="monthly"
                min_occurs=0,
                max_occurs=1,
                data_type="string",
            ),
            vector_name,
            log_level,
        ]

        outputs = [rda_output]

        super(ClimdexMMDMT, self).__init__(
            self._handler,
            identifier="climdex_mmdmt",
            title="Climdex MMDMT",
            abstract="Monthly or Annual Maximumof Daily Maximum Temperature",
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

    def MMDMT_type(self, month_type, ci, freq):
        climdex = get_package("climdex.pcic")

        if days_type == "txx":
            return climdex.climdex_txx(ci, freq)
        else:
            raise ValueError("invalid month_type")

    def _handler(self, request, response):
        climdex_input, ci_name, output_file, month_type, freq, vector_name, loglevel = [
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
            f"Processing {days_type} count",
            logger,
            log_level=loglevel,
            process_step="process",
        )
        temp = self.days(days_type, ci, freq)
        print(temp)

        log_handler(
            self,
            response,
            f"Saving {days_type} count as R data file",
            logger,
            log_level=loglevel,
            process_step="save_rdata",
        )
        output_path = os.path.join(self.workdir, output_file)
        save_python_to_rdata(vector_name, temp, output_path)

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
