import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_temp_pctl import ClimdexTempPctl


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "freq"),
    [
        (local_path("climdexInput.rda"), "ci", "tn10p", "monthly"),
        (local_path("climdexInput.rda"), "ci", "tn10p", "annual"),
        (local_path("climdexInput.rda"), "ci", "tn90p", "monthly"),
        (local_path("climdexInput.rda"), "ci", "tn90p", "annual"),
        (local_path("climdexInput.rda"), "ci", "tx10p", "monthly"),
        (local_path("climdexInput.rda"), "ci", "tx10p", "annual"),
        (local_path("climdexInput.rda"), "ci", "tx90p", "monthly"),
        (local_path("climdexInput.rda"), "ci", "tx90p", "annual"),
    ],
)
def test_wps_climdex_mmdmt(climdex_input, ci_name, func, freq):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"func={func};"
            f"freq={freq};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexTempPctl(), datainputs)
