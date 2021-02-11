import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_rmm import ClimdexRMM
from .common import build_file_input


def build_params(climdex_input, threshold, output_file):
    return (
        f"{build_file_input(climdex_input)};"
        f"threshold={threshold};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "threshold"),
    [
        (local_path("climdexInput.rda"), 10.0),
        (local_path("climdexInput.rda"), 20.0),
        (local_path("climdexInput.rds"), 15.5),
        (
            [
                local_path("climdexInput.rda"),
                local_path("climdexInput.rds"),
                local_path("climdex_input_multiple.rda"),
            ],
            3.0,
        ),
    ],
)
def test_wps_climdex_rmm(climdex_input, threshold):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, threshold, out_file.name)
        run_wps_process(ClimdexRMM(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "threshold"),
    [
        (local_path("expected_rmm.rda"), 10.0),
        (local_path("bad_file_tyoe.gz"), 20.0),
    ],
)
def test_wps_climdex_rmm_err(climdex_input, threshold):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, threshold, out_file.name)
        process_err_test(ClimdexRMM, datainputs)
