import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_rmm import ClimdexRMM


def build_params(climdex_input, ci_name, threshold, vector_name, output_file):
    return (
        f"climdex_input=@xlink:href={climdex_input};"
        f"ci_name={ci_name};"
        f"vector_name={vector_name};"
        f"threshold={threshold};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", 10.0, "vector_name"),
        (local_path("climdexInput.rda"), "ci", 20.0, "vector_name"),
        (local_path("climdexInput.rds"), "ci", 15.5, "vector_name"),
    ],
)
def test_wps_climdex_rmm(climdex_input, ci_name, threshold, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, threshold, vector_name, out_file.name
        )
        run_wps_process(ClimdexRMM(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "vector_name"),
    [(local_path("climdexInput.rda"), "ci", 10.0, "vector name",),],
)
def test_wps_climdex_rmm_vector_err(climdex_input, ci_name, threshold, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, threshold, vector_name, out_file.name
        )
        process_err_test(ClimdexRMM, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "vector_name"),
    [
        (local_path("climdexInput.rda"), "not_ci", 10.0, "vector_name",),
        (local_path("expected_rmm.rda"), "expected_r10mm", 20.0, "vector_name",),
    ],
)
def test_wps_climdex_rmm_ci_err(climdex_input, ci_name, threshold, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, threshold, vector_name, out_file.name
        )
        process_err_test(ClimdexRMM, datainputs)
