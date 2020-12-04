import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_days import ClimdexDays


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "days_type", "vector_name"),
    [
        (
            local_path("climdexInput.rda"), "ci", "summer", "summer_days",
        ),
        (
            local_path("climdexInput.rda"), "ci", "icing", "icing_days",
        ),
    ]
)
def test_wps_climdex_days(climdex_input, ci_name, days_type, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"days_type={days_type};"
            f"vector_name={vector_name};"
            f"output_path={out_file.name};"
        )
        run_wps_process(ClimdexDays(), datainputs)