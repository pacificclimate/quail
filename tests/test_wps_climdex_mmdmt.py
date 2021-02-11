import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_mmdmt import ClimdexMMDMT
from .common import build_file_input


def build_params(climdex_input, month_type, freq, output_file):
    return (
        f"{build_file_input(climdex_input)};"
        f"month_type={month_type};"
        f"freq={freq};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "month_type", "freq"),
    [
        (local_path("climdexInput.rda"), "txx", "monthly"),
        (local_path("climdexInput.rda"), "txx", "annual"),
        (local_path("climdexInput.rda"), "tnx", "monthly"),
        (local_path("climdexInput.rda"), "tnx", "annual"),
        (local_path("climdexInput.rds"), "txn", "monthly"),
        (local_path("climdexInput.rds"), "txn", "annual"),
        (local_path("climdexInput.rds"), "tnn", "monthly"),
        (local_path("climdexInput.rds"), "tnn", "annual"),
        (
            [
                local_path("climdexInput.rda"),
                local_path("climdexInput.rds"),
                local_path("climdex_input_multiple.rda"),
            ],
            "txx",
            "monthly",
        ),
    ],
)
def test_wps_climdex_mmdmt(climdex_input, month_type, freq):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, month_type, freq, out_file.name)
        run_wps_process(ClimdexMMDMT(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "month_type", "freq"),
    [
        (local_path("expected_mmdmt_data.rda"), "txx", "monthly"),
        (local_path("bad_file_type.gz"), "txx", "annual"),
    ],
)
def test_wps_climdex_mmdmt_err(climdex_input, month_type, freq):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, month_type, freq, out_file.name)
        process_err_test(ClimdexMMDMT, datainputs)
