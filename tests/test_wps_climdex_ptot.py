import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_ptot import ClimdexPtot


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "threshold"),
    [
        (local_path("climdexInput.rda"), "ci", 95),
    ],
)
def test_wps_climdex_spells(climdex_input, ci_name, threshold):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"threshold={threshold};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexPtot(), datainputs)
