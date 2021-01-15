import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_mmdmt import ClimdexMMDMT
from quail.utils import process_err_test

@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "month_type", "freq"),
    [
        (local_path("climdexInput.rda"), "ci", "txx", "monthly"),
        (local_path("climdexInput.rda"), "ci", "txx", "annual"),
        (local_path("climdexInput.rda"), "ci", "tnx", "monthly"),
        (local_path("climdexInput.rda"), "ci", "tnx", "annual"),
        (local_path("climdexInput.rda"), "ci", "txn", "monthly"),
        (local_path("climdexInput.rda"), "ci", "txn", "annual"),
        (local_path("climdexInput.rda"), "ci", "tnn", "monthly"),
        (local_path("climdexInput.rda"), "ci", "tnn", "annual"),
    ],
)
def test_wps_climdex_mmdmt(climdex_input, ci_name, month_type, freq):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"month_type={month_type};"
            f"freq={freq};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexMMDMT(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "month_type", "freq", "err_type"),
    [
        (local_path("climdexInput.rda"), "not_ci", "txx", "monthly", "unknown ci name"),
        (local_path("expected_mmdmt_data.rda"), "expected_tnx_annual", "tnx", "annual", "class is not ci"),

    ],
)
def test_wps_climdex_mmdmt_err(climdex_input, ci_name, month_type, freq, err_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"month_type={month_type};"
            f"freq={freq};"
            f"output_file={out_file.name};"
        )
        process_err_test(ClimdexMMDMT, datainputs, err_type)