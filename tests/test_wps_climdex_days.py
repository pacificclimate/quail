import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import local_path, run_wps_process, process_err_test
from quail.processes.wps_climdex_days import ClimdexDays


def build_params(climdex_input, ci_name, days_type, vector_name, output_file):
    return (
        f"climdex_input=@xlink:href={climdex_input};"
        f"ci_name={ci_name};"
        f"days_type={days_type};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )


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
            local_path("climdexInput.rds"),
            "ci",
            "frost days",
            "frost_days",
        ),
        (
            local_path("climdexInput.rds"),
            "ci",
            "tropical nights",
            "tropical_nights",
        ),
    ],
)
def test_wps_climdex_days(climdex_input, ci_name, days_type, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, days_type, vector_name, out_file.name
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
            climdex_input, ci_name, days_type, vector_name, out_file.name
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
            climdex_input, ci_name, days_type, vector_name, out_file.name
        )
        process_err_test(ClimdexDays, datainputs)
