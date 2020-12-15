import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_spells import ClimdexSpells


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "span_years"),
    [
        (local_path("climdexInput.rda"), "ci", "wsdi", False),
        (local_path("climdexInput.rda"), "ci", "wsdi", True),
        (local_path("climdexInput.rda"), "ci", "csdi", False),
        (local_path("climdexInput.rda"), "ci", "csdi", True),
        (local_path("climdexInput.rda"), "ci", "cdd", False),
        (local_path("climdexInput.rda"), "ci", "cdd", True),
    ],
)
def test_wps_climdex_spells(climdex_input, ci_name, func, span_years):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"func={func};"
            f"span_years={span_years};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexSpells(), datainputs)
