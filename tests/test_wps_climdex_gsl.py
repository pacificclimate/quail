import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_gsl import ClimdexGSL
from .common import build_file_input


def build_params(climdex_input, gsl_mode, output_file):
    return (
        f"{build_file_input(climdex_input)};"
        f"gsl_mode={gsl_mode};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "gsl_mode"),
    [
        (
            local_path("climdexInput.rda"),
            "GSL",
        ),
        (
            local_path("climdexInput.rda"),
            "GSL_first",
        ),
        (
            local_path("climdexInput.rds"),
            "GSL_max",
        ),
        (
            local_path("climdexInput.rds"),
            "GSL_sum",
        ),
        (
            [
                local_path("climdexInput.rda"),
                local_path("climdexInput.rds"),
                local_path("climdex_input_multiple.rda"),
            ],
            "GSL",
        ),
    ],
)
def test_wps_climdex_gsl(climdex_input, gsl_mode):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, gsl_mode, out_file.name)
        run_wps_process(ClimdexGSL(), datainputs)
