import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_spells import ClimdexSpells
from .common import build_file_input


def build_params(climdex_input, func, span_years, output_file):
    return (
        f"{build_file_input(climdex_input)}"
        f"func={func};"
        f"span_years={span_years};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "func", "span_years"),
    [
        (local_path("climdexInput.rda"), "wsdi", False),
        (local_path("climdexInput.rda"), "wsdi", True),
        (local_path("climdexInput.rda"), "csdi", False),
        (local_path("climdexInput.rda"), "csdi", True),
        (local_path("climdexInput.rds"), "cdd", False),
        (local_path("climdexInput.rds"), "cdd", True),
        (local_path("climdexInput.rds"), "cwd", False),
        (local_path("climdexInput.rds"), "cwd", True),
        (local_path("climdexInput.rds"), "wsdi", False),
        (
            [
                local_path("climdexInput.rda"),
                local_path("climdexInput.rds"),
                local_path("climdex_input_multiple.rda"),
            ],
            "wsdi",
            False,
        ),
    ],
)
def test_wps_climdex_spells(climdex_input, func, span_years):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, func, span_years, out_file.name)
        run_wps_process(ClimdexSpells(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "func", "span_years"),
    [
        (local_path("expected_spells_data.rda"), "wsdi", False),
        (local_path("bad_file_type.gz"), "wsdi", True),
    ],
)
def test_wps_climdex_spells_err(climdex_input, func, span_years):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(climdex_input, func, span_years, out_file.name)
        process_err_test(ClimdexSpells, datainputs)
