import pytest
import io
from tempfile import NamedTemporaryFile
from contextlib import redirect_stderr

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_dtr import ClimdexDTR
from quail.utils import process_err_test

@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq"),
    [
        (local_path("climdexInput.rda"), "ci", "monthly"),
        (local_path("climdexInput.rda"), "ci", "annual"),
    ],
)
def test_wps_climdex_dtr(climdex_input, ci_name, freq):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"freq={freq};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexDTR(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "freq", "err_type"),
    [
        (local_path("climdexInput.rda"), "not_ci", "monthly", "unknown ci name"),
        (local_path("expected_dtr.rda"), "expected_dtr_annual", "annual", "class is not ci"),
    ],
)
def test_wps_climdex_dtr_err(climdex_input, ci_name, freq, err_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"freq={freq};"
            f"output_file={out_file.name};"
        )
        process_err_test(ClimdexDTR, datainputs, err_type)