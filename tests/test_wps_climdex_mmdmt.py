import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_mmdmt import ClimdexMMDMT


def build_params(climdex_input, ci_name, month_type, freq, vector_name, output_file):
    return (
        f"climdex_input=@xlink:href={climdex_input};"
        f"ci_name={ci_name};"
        f"month_type={month_type};"
        f"vector_name={vector_name};"
        f"freq={freq};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "month_type", "freq", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "txx", "monthly", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "txx", "annual", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "tnx", "monthly", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "tnx", "annual", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "txn", "monthly", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "txn", "annual", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "tnn", "monthly", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "tnn", "annual", "vector_name"),
    ],
)
def test_wps_climdex_mmdmt(climdex_input, ci_name, month_type, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, month_type, freq, vector_name, out_file.name
        )
        run_wps_process(ClimdexMMDMT(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "month_type", "freq", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "txx",
            "monthly",
            "vector name",
        ),
    ],
)
def test_wps_climdex_mmdmt_vector_err(
    climdex_input, ci_name, month_type, freq, vector_name
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, month_type, freq, vector_name, out_file.name
        )
        process_err_test(ClimdexMMDMT, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "month_type", "freq", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "txx",
            "monthly",
            "vector_name",
        ),
        (
            local_path("expected_mmdmt_data.rda"),
            "expected_tnx_annual",
            "tnx",
            "annual",
            "vector_name",
        ),
    ],
)
def test_wps_climdex_mmdmt_ci_err(
    climdex_input, ci_name, month_type, freq, vector_name
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, month_type, freq, vector_name, out_file.name
        )
        process_err_test(ClimdexMMDMT, datainputs)
