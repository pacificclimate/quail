import pytest
import io
from tempfile import NamedTemporaryFile
from contextlib import redirect_stderr

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_dtr import ClimdexDTR


def build_params(ci_name, freq, vector_name, output_file, ci_rda=None, ci_rds=None):
    params = (
        f"ci_name={ci_name};"
        f"vector_name={vector_name};"
        f"freq={freq};"
        f"output_file={output_file};"
    )
    if ci_rda:
        return params + f"ci_rda=@xlink:href={ci_rda};"
    elif ci_rds:
        return params + f"ci_rds=@xlink:href={ci_rds};"


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "monthly", "dtr"),
        (local_path("climdexInput.rda"), "ci", "annual", "dtr"),
    ],
)
def test_wps_climdex_dtr_rda(climdex_input, ci_name, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, freq, vector_name, out_file.name, ci_rda=climdex_input
        )
        run_wps_process(ClimdexDTR(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "vector_name"),
    [
        (local_path("climdexInput.rds"), "ci", "monthly", "dtr"),
        (local_path("climdexInput.rds"), "ci", "annual", "dtr"),
    ],
)
def test_wps_climdex_dtr_rds(climdex_input, ci_name, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, freq, vector_name, out_file.name, ci_rds=climdex_input
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
            ci_name, freq, vector_name, out_file.name, ci_rda=climdex_input
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
            ci_name, freq, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexDTR, datainputs)
