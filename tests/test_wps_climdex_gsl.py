import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_gsl import ClimdexGSL
from quail.utils import process_err_test


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "gsl_mode"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "GSL",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "GSL_first",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "GSL_max",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "GSL_sum",
        ),
    ],
)
def test_wps_climdex_gsl(climdex_input, ci_name, gsl_mode):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"gsl_mode={gsl_mode};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexGSL(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "gsl_mode", "vector_name", "err_type"),
    [
        (local_path("climdexInput.rda"), "not_ci", "GSL", "vector_name", "unknown ci name"),
        (local_path("climdexInput.rda"), "ci", "GSL", "vector name", "invalid vector name"),
        (
            local_path("expected_gsl.rda"),
            "expected_gsl_vector",
            "GSL",
            "vector_name",
            "class is not ci",
        ),
    ],
)
def test_wps_climdex_gsl_err(climdex_input, ci_name, gsl_mode, err_type, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"vector_name={vector_name};"
            f"gsl_mode={gsl_mode};"
            f"output_file={out_file.name};"
        )
        process_err_test(ClimdexGSL, datainputs, err_type)
