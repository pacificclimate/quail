import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_sdii import ClimdexSDII
from quail.utils import process_err_test


@pytest.mark.parametrize(
    ("climdex_input", "ci_name"),
    [
        (local_path("climdexInput.rda"), "ci"),
    ],
)
def test_wps_climdex_sdii(climdex_input, ci_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexSDII(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "err_type"),
    [
        (local_path("climdexInput.rda"), "not_ci", "unknown ci name"),
        (local_path("expected_sdii.rda"), "expected_sdii", "class is not ci"),
    ],
)
def test_wps_climdex_sdii_err(climdex_input, ci_name, err_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"output_file={out_file.name};"
        )
        process_err_test(ClimdexSDII, datainputs, err_type)