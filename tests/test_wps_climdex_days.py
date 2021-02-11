import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import local_path, run_wps_process, process_err_test
from quail.processes.wps_climdex_days import ClimdexDays
from .common import build_file_input


def build_params(climdex_input, days_type, output_file):
    return (
        f"{build_file_input(climdex_input)}"
        f"days_type={days_type};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "days_type"),
    [
        (
            local_path("climdexInput.rda"),
            "su",
        ),
        (
            local_path("climdexInput.rda"),
            "id",
        ),
        (
            local_path("climdexInput.rds"),
            "fd",
        ),
        (
            local_path("climdexInput.rds"),
            "tr",
        ),
        (
            [
                local_path("climdexInput.rds"),
                local_path("climdexInput.rda"),
                local_path("climdex_input_multiple.rda"),
            ],
            "su",
        ),
    ],
)
def test_wps_climdex_days(climdex_input, days_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, days_type, out_file.name)
        run_wps_process(ClimdexDays(), datainputs)
