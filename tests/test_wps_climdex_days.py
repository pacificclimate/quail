import pytest
import io
from tempfile import NamedTemporaryFile
from pywps.app.exceptions import ProcessError
from contextlib import redirect_stderr

from wps_tools.testing import local_path, run_wps_process, process_err_test
from quail.processes.wps_climdex_days import ClimdexDays


def build_params(
    ci_name, days_type, vector_name, output_file, ci_rda=None, ci_rds=None
):
    params = (
        f"ci_name={ci_name};"
        f"days_type={days_type};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )
    if ci_rda:
        return params + f"ci_rda=@xlink:href={ci_rda};"
    elif ci_rds:
        return params + f"ci_rds=@xlink:href={ci_rds};"
    else:
        raise Exception("Need one of ci_rda or ci_rds")


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "days_type", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "summer days",
            "summer_days",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "icing days",
            "icing_days",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "frost days",
            "frost_days",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "tropical nights",
            "tropical_nights",
        ),
    ],
)
def test_wps_climdex_days_rda(climdex_input, ci_name, days_type, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, days_type, vector_name, out_file.name, ci_rda=climdex_input
        )
        run_wps_process(ClimdexDays(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "days_type", "vector_name"),
    [
        (local_path("climdexInput.rds"), "ci_name", "summer days", "vector_name"),
    ],
)
def test_wps_climdex_days_rds(climdex_input, ci_name, days_type, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, days_type, vector_name, out_file.name, ci_rds=climdex_input
        )
        run_wps_process(ClimdexDays(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "days_type", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "summer days",
            "summer days",
        ),
    ],
)
def test_wps_climdex_days_vector_err(climdex_input, ci_name, days_type, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, days_type, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexDays, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "days_type", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "summer days",
            "summer_days",
        ),
        (
            local_path("expected_days_data.rda"),
            "expected_summer_days",
            "summer days",
            "summer_days",
        ),
    ],
)
def test_wps_climdex_days_ci_err(climdex_input, ci_name, days_type, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, days_type, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexDays, datainputs)
