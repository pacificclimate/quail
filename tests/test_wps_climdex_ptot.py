import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_ptot import ClimdexPtot


def buil_params(ci_name, threshold, vector_name, output_file, ci_rda=None, ci_rds=None):
    params = (
        f"ci_name={ci_name};"
        f"output_file={output_file};"
        f"vector_name={vector_name};"
    )
    if ci_rda:
        params += f"ci_rda=@xlink:href={ci_rda};"
    elif ci_rds:
        params += f"ci_rds=@xlink:href={ci_rds};"

    if threshold:
        params += f"threshold={threshold};"

    return params


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", None, "vector_name"),
        (local_path("climdexInput.rda"), "ci", 95, "vector_name"),
        (local_path("climdexInput.rda"), "ci", 99, "vector_name"),
    ],
)
def test_wps_climdex_ptot_rda(climdex_input, ci_name, threshold, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = buil_params(
            ci_name, threshold, vector_name, out_file.name, ci_rda=climdex_input
        )
        run_wps_process(ClimdexPtot(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "vector_name"),
    [
        (local_path("climdexInput.rds"), "ci", None, "vector_name"),
    ],
)
def test_wps_climdex_ptot_rds(climdex_input, ci_name, threshold, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = buil_params(
            ci_name, threshold, vector_name, out_file.name, ci_rds=climdex_input
        )
        run_wps_process(ClimdexPtot(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            95,
            "vector name",
        ),
    ],
)
def test_wps_climdex_ptot_vector_err(climdex_input, ci_name, threshold, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = buil_params(
            ci_name, threshold, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexPtot, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            95,
            "vector_name",
        ),
        (
            local_path("expected_ptot.rda"),
            "expected_r99ptot",
            99,
            "vector_name",
        ),
    ],
)
def test_wps_climdex_ptot_ci_err(climdex_input, ci_name, threshold, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = buil_params(
            ci_name, threshold, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexPtot, datainputs)
