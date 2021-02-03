import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_spells import ClimdexSpells


def build_params(climdex_input, ci_name, func, span_years, vector_name, output_file):
    return (
        f"climdex_input=@xlink:href={climdex_input};"
        f"ci_name={ci_name};"
        f"func={func};"
        f"span_years={span_years};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "span_years", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "wsdi", False, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "wsdi", True, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "csdi", False, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "csdi", True, "vector_name"),
        (local_path("climdexInput.rds"), "ci", "cdd", False, "vector_name"),
        (local_path("climdexInput.rds"), "ci", "cdd", True, "vector_name"),
        (local_path("climdexInput.rds"), "ci", "cwd", False, "vector_name"),
        (local_path("climdexInput.rds"), "ci", "cwd", True, "vector_name"),
        (local_path("climdexInput.rds"), "ci", "wsdi", False, "vector_name"),
    ],
)
def test_wps_climdex_spells_rds(climdex_input, ci_name, func, span_years, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, func, span_years, vector_name, out_file.name
        )
        run_wps_process(ClimdexSpells(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "span_years", "vector_name"),
    [(local_path("climdexInput.rda"), "ci", "wsdi", False, "vector name",),],
)
def test_wps_climdex_spells_vector_err(
    climdex_input, ci_name, func, span_years, vector_name
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, func, span_years, vector_name, out_file.name
        )
        process_err_test(ClimdexSpells, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "span_years", "vector_name"),
    [
        (local_path("climdexInput.rda"), "not_ci", "wsdi", False, "vector_name",),
        (
            local_path("expected_spells_data.rda"),
            "expected_csdi_span_yrs",
            "csdi",
            True,
            "vector_name",
        ),
    ],
)
def test_wps_climdex_spells_ci_err(
    climdex_input, ci_name, func, span_years, vector_name
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            climdex_input, ci_name, func, span_years, vector_name, out_file.name
        )
        process_err_test(ClimdexSpells, datainputs)
