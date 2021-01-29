import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_rxnday import ClimdexRxnday


def build_params(climdex_input, ci_name, freq, num_days, vector_name, output_file):
    return (
        f"climdex_input=@xlink:href={climdex_input};"
        f"ci_name={ci_name};"
        f"vector_name={vector_name}"
        f"freq={freq};"
        f"num_days={num_days};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "num_days", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "monthly", 1, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "annual", 1, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "monthly", 5, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "annual", 5, "vector_name"),
    ],
)
def test_wps_climdex_rxnday(climdex_input, ci_name, freq, num_days, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, freq, num_days, vector_name, out_file.name
        )
        run_wps_process(ClimdexRxnday(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "num_days", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "monthly",
            1,
            "vector_name",
        ),
        (
            local_path("expected_rxnday.rda"),
            "expected_rx5day_annual",
            "annual",
            5,
            "vector_name",
        ),
    ],
)
def test_wps_climdex_rxnday_ci_err(climdex_input, ci_name, freq, num_days, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, freq, num_days, vector_name, out_file.name
        )
        process_err_test(ClimdexRxnday, datainputs)
