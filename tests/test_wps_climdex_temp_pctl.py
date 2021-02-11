import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_temp_pctl import ClimdexTempPctl
from .common import build_file_input


def build_params(climdex_input, func, freq, output_file):
    return (
        f"{build_file_input(climdex_input)}"
        f"func={func};"
        f"freq={freq};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "func", "freq"),
    [
        (local_path("climdexInput.rda"), "tn10p", "monthly"),
        (local_path("climdexInput.rda"), "tn10p", "annual"),
        (local_path("climdexInput.rda"), "tn90p", "monthly"),
        (local_path("climdexInput.rda"), "tn90p", "annual"),
        (local_path("climdexInput.rds"), "tx10p", "monthly"),
        (local_path("climdexInput.rds"), "tx10p", "annual"),
        (local_path("climdexInput.rds"), "tx90p", "monthly"),
        (local_path("climdexInput.rds"), "tx90p", "annual"),
        (
            [
                local_path("climdexInput.rda"),
                local_path("climdexInput.rds"),
                local_path("climdex_input_multiple.rda"),
            ],
            "tn10p",
            "monthly",
        ),
    ],
)
def test_wps_climdex_temp_pctl(climdex_input, func, freq):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, func, freq, out_file.name)
        run_wps_process(ClimdexTempPctl(), datainputs)
