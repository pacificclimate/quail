import pytest
from tempfile import NamedTemporaryFile
from pkg_resources import resource_filename

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_fd import ClimdexFD


@pytest.mark.parametrize(
    ("ci_file", "ci_name", "output_obj"),
    [(local_path("climdexInput.rda"), "ci", "fd")],
)
def test_wps_climdex_fd(ci_file, ci_name, output_obj):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"ci_file=@xlink:href={ci_file};"
            f"ci_name={ci_name};"
            f"output_obj={output_obj};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexFD(), datainputs)
