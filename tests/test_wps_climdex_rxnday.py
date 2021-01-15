import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_rxnday import ClimdexRxnday
from quail.utils import process_err_test


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "num_days"),
    [
        (local_path("climdexInput.rda"), "ci", "monthly", 1),
        (local_path("climdexInput.rda"), "ci", "annual", 1),
        (local_path("climdexInput.rda"), "ci", "monthly", 5),
        (local_path("climdexInput.rda"), "ci", "annual", 5),
    ],
)
def test_wps_climdex_rxnday(climdex_input, ci_name, freq, num_days):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"freq={freq};"
            f"num_days={num_days};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexRxnday(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "num_days", "err_type"),
    [
        (local_path("climdexInput.rda"), "not_ci", "monthly", 1, "unknown ci name"),
        (
            local_path("expected_rxnday.rda"),
            "expected_rx5day_annual",
            "annual",
            5,
            "class is not ci",
        ),
    ],
)
def test_wps_climdex_rxnday_err(climdex_input, ci_name, freq, num_days, err_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"freq={freq};"
            f"num_days={num_days};"
            f"output_file={out_file.name};"
        )
        process_err_test(ClimdexRxnday, datainputs, err_type)
