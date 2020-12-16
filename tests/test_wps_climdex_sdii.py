import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_sdii import ClimdexSDII


@pytest.mark.parametrize(
    ("climdex_input", "ci_name"),
    [
        (local_path("climdexInput.rda"), "ci"),
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
