import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_dtr import ClimdexDTR
from .common import build_file_input


def build_params(climdex_input, freq, output_file):
    return (
        f"{build_file_input(climdex_input)}"
        f"freq={freq};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "freq"),
    [
        (local_path("climdexInput.rda"), "monthly"),
        (local_path("climdexInput.rda"), "annual"),
        (local_path("climdexInput.rds"), "annual"),
        (
            [
                local_path("climdexInput.rda"),
                local_path("climdexInput.rds"),
                local_path("climdex_input_multiple.rda"),
            ],
            "monthly",
        ),
    ],
)
def test_wps_climdex_dtr(climdex_input, freq):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, freq, out_file.name)
        run_wps_process(ClimdexDTR(), datainputs)
