import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_rmm import ClimdexRMM
from quail.utils import process_err_test


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold"),
    [
        (local_path("climdexInput.rda"), "ci", 10.0),
        (local_path("climdexInput.rda"), "ci", 20.0),
        (local_path("climdexInput.rda"), "ci", 15.5),
    ],
)
def test_wps_climdex_rmm(climdex_input, ci_name, threshold):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"threshold={threshold};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexRMM(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "err_type"),
    [
        (local_path("climdexInput.rda"), "not_ci", 10.0, "unknown ci name"),
        (local_path("expected_rmm.rda"), "expected_r10mm", 20.0, "class is not ci"),
    ],
)
def test_wps_climdex_rmm_err(climdex_input, ci_name, threshold, err_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"threshold={threshold};"
            f"output_file={out_file.name};"
        )
        process_err_test(ClimdexRMM, datainputs, err_type)
