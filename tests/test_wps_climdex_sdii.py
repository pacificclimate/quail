import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_sdii import ClimdexSDII


def build_params(climdex_input, ci_name, vector_name, output_file):
    return (
        f"climdex_input=@xlink:href={climdex_input};"
        f"ci_name={ci_name};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "vector_name"),
        (local_path("climdexInput.rds"), "ci", "vector_name"),
    ],
)
def test_wps_climdex_sdii(climdex_input, ci_name, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, ci_name, vector_name, out_file.name)
        run_wps_process(ClimdexSDII(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "vector name",
        ),
    ],
)
def test_wps_climdex_sdii_vector_err(climdex_input, ci_name, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, ci_name, vector_name, out_file.name)
        process_err_test(ClimdexSDII, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "vector_name",
        ),
        (
            local_path("expected_sdii.rda"),
            "expected_sdii",
            "vector_name",
        ),
    ],
)
def test_wps_climdex_sdii_ci_err(climdex_input, ci_name, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, ci_name, vector_name, out_file.name)
        process_err_test(ClimdexSDII, datainputs)
