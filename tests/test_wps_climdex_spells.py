import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_spells import ClimdexSpells


def build_params(
    ci_name, func, span_years, vector_name, output_file, ci_rda=None, ci_rds=None
):
    params = (
        f"ci_name={ci_name};"
        f"func={func};"
        f"span_years={span_years};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )
    if ci_rda:
        return params + f"ci_rda=@xlink:href={ci_rda};"
    elif ci_rds:
        return params + f"ci_rds=@xlink:href={ci_rds};"


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "span_years", "vector_name"),
    [
        (local_path("climdexInput.rda"), "ci", "wsdi", False, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "wsdi", True, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "csdi", False, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "csdi", True, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "cdd", False, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "cdd", True, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "cwd", False, "vector_name"),
        (local_path("climdexInput.rda"), "ci", "cwd", True, "vector_name"),
    ],
)
def test_wps_climdex_spells_rda(climdex_input, ci_name, func, span_years, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, func, span_years, vector_name, out_file.name, ci_rda=climdex_input
        )
        run_wps_process(ClimdexSpells(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "span_years", "vector_name"),
    [
        (local_path("climdexInput.rds"), "ci", "wsdi", False, "vector_name"),
    ],
)
def test_wps_climdex_spells_rds(climdex_input, ci_name, func, span_years, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, func, span_years, vector_name, out_file.name, ci_rds=climdex_input
        )
        run_wps_process(ClimdexSpells(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "span_years", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "ci",
            "wsdi",
            False,
            "vector name",
        ),
    ],
)
def test_wps_climdex_spells_vector_err(
    climdex_input, ci_name, func, span_years, vector_name
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            ci_name, func, span_years, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexSpells, datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "func", "span_years", "vector_name"),
    [
        (
            local_path("climdexInput.rda"),
            "not_ci",
            "wsdi",
            False,
            "vector_name",
        ),
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
            ci_name, func, span_years, vector_name, out_file.name, ci_rda=climdex_input
        )
        process_err_test(ClimdexSpells, datainputs)
