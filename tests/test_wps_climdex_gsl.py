import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_gsl import ClimdexGSL


def build_params(ci_name, vector_name, gsl_mode, output_file, ci_rda=None, ci_rds=None):
    params = (
        f"ci_name={ci_name};"
        f"vector_name={vector_name};"
        f"gsl_mode={gsl_mode};"
        f"output_file={output_file};"
    )
    if ci_rda:
        return params + f"ci_rda=@xlink:href={ci_rda};"
    elif ci_rds:
        return params + f"ci_rds=@xlink:href={ci_rds};"


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "vector_name", "gsl_mode"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "vector_name",
            "GSL",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "vector_name",
            "GSL_first",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "vector_name",
            "GSL_max",
        ),
        (
            local_path("climdexInput.rda"),
            "ci",
            "vector_name",
            "GSL_sum",
        ),
    ],
)
def test_wps_climdex_gsl_rda(climdex_input, ci_name, vector_name, gsl_mode):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, vector_name, gsl_mode, out_file.name, ci_rda=climdex_input
        )
        run_wps_process(ClimdexGSL(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "vector_name", "gsl_mode"),
    [
        (
            local_path("climdexInput.rds"),
            "ci",
            "vector_name",
            "GSL",
        ),
    ],
)
def test_wps_climdex_gsl_rds(climdex_input, ci_name, vector_name, gsl_mode):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, vector_name, gsl_mode, out_file.name, ci_rds=climdex_input
        )
        run_wps_process(ClimdexGSL(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "gsl_mode", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "GSL",
            "vector name",
        ),
    ],
)
def test_wps_climdex_gsl_vector_err(climdex_input, ci_name, gsl_mode, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, vector_name, gsl_mode, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexGSL, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "gsl_mode", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "GSL",
            "vector_name",
        ),
        (
            local_path("expected_gsl.rda"),
            "expected_gsl_vector",
            "GSL",
            "vector_name",
        ),
    ],
)
def test_wps_climdex_gsl_ci_err(climdex_input, ci_name, gsl_mode, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, vector_name, gsl_mode, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexGSL, datainputs)
