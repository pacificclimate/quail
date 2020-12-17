import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_get_available_indices import ClimdexGetAvailableIndices


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "get_function_names"),
    [
        (local_path("climdexInput.rda"), "ci", True),
        (local_path("climdexInput.rda"), "ci", False),
    ],
)
def test_wps_get_available_indices(climdex_input, ci_name, get_function_names):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"get_function_names={get_function_names};"
            f"output_file={out_file.name};"
        )
        run_wps_process(ClimdexGetAvailableIndices(), datainputs)
