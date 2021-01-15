import pytest
import io
from tempfile import NamedTemporaryFile
from pywps.app.exceptions import ProcessError
from contextlib import redirect_stderr

from wps_tools.testing import local_path, run_wps_process
from quail.processes.wps_climdex_days import ClimdexDays
from quail.utils import process_err_test


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
def test_wps_climdex_days(climdex_input, ci_name, days_type, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"days_type={days_type};"
            f"vector_name={vector_name};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexDays(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "days_type", "vector_name", "err_type"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "summer days",
            "summer_days",
            "unknown ci name",
        ),
        (
            local_path("expected_days_data.rda"),
            "expected_summer_days",
            "summer days",
            "summer_days",
            "class is not ci",
        ),
    ],
)
def test_wps_climdex_days_err(climdex_input, ci_name, days_type, vector_name, err_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"days_type={days_type};"
            f"vector_name={vector_name};"
            f"output_file={out_file.name};"
        )
        process_err_test(ClimdexDays, datainputs, err_type)
