import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_sdii import ClimdexSDII


def build_params(ci_name, vector_name, output_file, ci_rda=None, ci_rds=None):
    params = (
        f"ci_name={ci_name};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )
    if ci_rda:
        return params + f"ci_rda=@xlink:href={ci_rda};"
    elif ci_rds:
        return params + f"ci_rds=@xlink:href={ci_rds};"


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "vector_name"),
    ],
)
def test_wps_climdex_sdii_rda(climdex_input, ci_name, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, vector_name, out_file.name, ci_rda=climdex_input
        )
        run_wps_process(ClimdexSDII(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "vector_name"),
    [
        (local_path("climdexInput.rds"), "ci", "vector_name"),
    ],
)
def test_wps_climdex_sdii_rds(climdex_input, ci_name, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, vector_name, out_file.name, ci_rds=climdex_input
        )
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
        datainputs = build_params(
            ci_name, vector_name, out_file.name, ci_rda=climdex_input
        )
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
        datainputs = build_params(
            ci_name, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexSDII, datainputs)
