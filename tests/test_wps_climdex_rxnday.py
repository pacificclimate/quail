import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_rxnday import ClimdexRxnday


def build_params(
    ci_name, freq, num_days, vector_name, output_file, ci_rda=None, ci_rds=None
):
    params = (
        f"ci_name={ci_name};"
        f"vector_name={vector_name}"
        f"freq={freq};"
        f"num_days={num_days};"
        f"output_file={output_file};"
    )
    if ci_rda:
        return params + f"ci_rda=@xlink:href={ci_rda};"
    elif ci_rds:
        return params + f"ci_rds=@xlink:href={ci_rds};"


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "num_days", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "monthly", 1, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "annual", 1, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "monthly", 5, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "annual", 5, "vector_name"),
    ],
)
def test_wps_climdex_rxnday_rda(climdex_input, ci_name, freq, num_days, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, freq, num_days, vector_name, out_file.name, ci_rda=climdex_input
        )
        run_wps_process(ClimdexRxnday(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "num_days", "vector_name"),
    [
        (local_path("climdexInput.rds"), "ci", "monthly", 1, "vector_name"),
    ],
)
def test_wps_climdex_rxnday_rds(climdex_input, ci_name, freq, num_days, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, freq, num_days, vector_name, out_file.name, ci_rds=climdex_input
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
            ci_name, freq, num_days, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexRxnday, datainputs)
