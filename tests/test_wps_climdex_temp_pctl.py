import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_temp_pctl import ClimdexTempPctl


def build_params(climdex_input, ci_name, func, freq, vector_name, output_file):
    return (
        f"climdex_input=@xlink:href={climdex_input};"
        f"ci_name={ci_name};"
        f"func={func};"
        f"freq={freq};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "freq", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "tn10p", "monthly", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "tn10p", "annual", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "tn90p", "monthly", "vector_name"),
        (local_path("climdexInput.rda"), "ci", "tn90p", "annual", "vector_name"),
        (local_path("climdexInput.rds"), "ci", "tx10p", "monthly", "vector_name"),
        (local_path("climdexInput.rds"), "ci", "tx10p", "annual", "vector_name"),
        (local_path("climdexInput.rds"), "ci", "tx90p", "monthly", "vector_name"),
        (local_path("climdexInput.rds"), "ci", "tx90p", "annual", "vector_name"),
    ],
)
def test_wps_climdex_temp_pctl(climdex_input, ci_name, func, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, func, freq, vector_name, out_file.name
        )
        run_wps_process(ClimdexTempPctl(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "freq", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "tn10p",
            "monthly",
            "vector name",
        ),
    ],
)
def test_wps_climdex_temp_pctl_vector_err(
    climdex_input, ci_name, func, freq, vector_name
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, func, freq, vector_name, out_file.name
        )
        process_err_test(ClimdexTempPctl, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "freq", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "tn10p",
            "monthly",
            "vector_name",
        ),
        (
            local_path("expected_temp_pctl.rda"),
            "expected_tn90p",
            "tn90p",
            "annual",
            "vector_name",
        ),
    ],
)
def test_wps_climdex_temp_pctl_ci_err(climdex_input, ci_name, func, freq, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, func, freq, vector_name, out_file.name
        )
        process_err_test(ClimdexTempPctl, datainputs)
