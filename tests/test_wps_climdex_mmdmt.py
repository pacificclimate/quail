import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_mmdmt import ClimdexMMDMT


def build_params(
    ci_name, month_type, freq, vector_name, output_file, ci_rda=None, ci_rds=None
):
    params = (
        f"ci_name={ci_name};"
        f"month_type={month_type};"
        f"vector_name={vector_name};"
        f"freq={freq};"
        f"output_file={output_file};"
    )
    if ci_rda:
        return params + f"ci_rda=@xlink:href={ci_rda};"
    elif ci_rds:
        return params + f"ci_rds=@xlink:href={ci_rds};"


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
def test_wps_climdex_mmdmt_rda(climdex_input, ci_name, month_type, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, month_type, freq, vector_name, out_file.name, ci_rda=climdex_input
        )
        run_wps_process(ClimdexMMDMT(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "month_type", "freq", "vector_name"),
    [
        (local_path("climdexInput.rds"), "ci", "txx", "monthly", "vector_name"),
    ],
)
def test_wps_climdex_mmdmt_rds(climdex_input, ci_name, month_type, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, month_type, freq, vector_name, out_file.name, ci_rds=climdex_input
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
            ci_name, month_type, freq, vector_name, out_file.name, ci_rda=climdex_input
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
            ci_name, month_type, freq, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexMMDMT, datainputs)
