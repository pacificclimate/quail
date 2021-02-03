import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_dtr import ClimdexDTR


def build_params(climdex_input, ci_name, freq, vector_name, output_file):
    return (
        f"climdex_input=@xlink:href={climdex_input};"
        f"ci_name={ci_name};"
        f"vector_name={vector_name};"
        f"freq={freq};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "monthly", "dtr"),
        (local_path("climdexInput.rda"), "ci", "annual", "dtr"),
        (local_path("climdexInput.rds"), "ci", "annual", "dtr"),
    ],
)
def test_wps_climdex_dtr(climdex_input, ci_name, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, freq, vector_name, out_file.name
        )
        run_wps_process(ClimdexDTR(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "monthly",
            "vector name",
        ),
    ],
)
def test_wps_climdex_dtr_vector_err(climdex_input, ci_name, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, freq, vector_name, out_file.name
        )
        process_err_test(ClimdexDTR, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "monthly",
            "vector_name",
        ),
        (
            local_path("expected_dtr.rda"),
            "expected_dtr_annual",
            "annual",
            "vector_name",
        ),
    ],
)
def test_wps_climdex_dtr_ci_err(climdex_input, ci_name, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, freq, vector_name, out_file.name
        )
        process_err_test(ClimdexDTR, datainputs)
