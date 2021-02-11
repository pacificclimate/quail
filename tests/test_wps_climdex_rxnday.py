import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_rxnday import ClimdexRxnday
from .common import build_file_input


def build_params(climdex_input, freq, num_days, output_file):
    return (
        f"{build_file_input(climdex_input)};"
        f"num_days={num_days};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "freq", "num_days"),
    [
        (local_path("climdexInput.rda"), "monthly", 1),
        (local_path("climdexInput.rda"), "annual", 1),
        (local_path("climdexInput.rds"), "monthly", 5),
        (local_path("climdexInput.rds"), "annual", 5),
        (
            [
                local_path("climdexInput.rda"),
                local_path("climdexInput.rds"),
                local_path("climdex_input_multiple.rda"),
            ],
            "monthly",
            5,
        ),
    ],
)
def test_wps_climdex_rxnday(climdex_input, freq, num_days):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, freq, num_days, out_file.name)
        run_wps_process(ClimdexRxnday(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "freq", "num_days"),
    [
        (local_path("expected_rxnday.rda"), "monthly", 1),
        (local_path("bad_file_type.gz"), "annual", 1),
    ],
)
def test_wps_climdex_rxnday_err(climdex_input, freq, num_days):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, freq, num_days, out_file.name)
        process_err_test(ClimdexRxnday, datainputs)
