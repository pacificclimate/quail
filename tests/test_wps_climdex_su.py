import pytest
from tempfile import NamedTemporaryFile
from pkg_resources import resource_filename

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_su import ClimdexSU


@pytest.mark.parametrize(
    ("climdex_input"),
    [local_path("climdexInput.rda")],
)
def test_wps_climdex_su(climdex_input):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = f"climdex_input=@xlink:href={climdex_input};" f"output_path={out_file.name};"
        run_wps_process(ClimdexSU(), datainputs)
