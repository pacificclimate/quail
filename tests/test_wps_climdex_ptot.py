import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_ptot import ClimdexPtot
from quail.utils import process_err_test


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold"),
    [
        (local_path("climdexInput.rda"), "ci", None),
        (local_path("climdexInput.rda"), "ci", 95),
        (local_path("climdexInput.rda"), "ci", 99),
    ],
)
def test_wps_climdex_ptot(climdex_input, ci_name, threshold):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"output_file={out_file.name};"
        )

        if threshold:
            datainputs += f"threshold={threshold};"

        run_wps_process(ClimdexPtot(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold", "err_type"),
    [
        (local_path("climdexInput.rda"), "not_ci", 95, "unknown ci name"),
        (local_path("expected_ptot.rda"), "expected_r99ptot", 99, "class is not ci"),
    ],
)
def test_wps_climdex_ptot_err(climdex_input, ci_name, threshold, err_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"output_file={out_file.name};"
            f"threshold={threshold};"
        )
        process_err_test(ClimdexPtot, datainputs, err_type)
