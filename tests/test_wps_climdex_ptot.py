import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_ptot import ClimdexPtot
from .common import build_file_input


def build_params(climdex_input, threshold, output_file):
    params = f"{build_file_input(climdex_input)};" f"output_file={output_file};"
    if threshold:
        params += f"threshold={threshold};"

    return params


@pytest.mark.parametrize(
    ("climdex_input", "threshold"),
    [
        (local_path("climdexInput.rda"), None),
        (local_path("climdexInput.rda"), 95),
        (local_path("climdexInput.rda"), 99),
        (local_path("climdexInput.rds"), None),
        (local_path("climdexInput.rds"), 99),
        (
            [
                local_path("climdexInput.rda"),
                local_path("climdexInput.rds"),
                local_path("climdex_input_multiple.rda"),
            ],
            95,
        ),
    ],
)
def test_wps_climdex_ptot_single(climdex_input, threshold):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, threshold, out_file.name)
        run_wps_process(ClimdexPtot(), datainputs)
