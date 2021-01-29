import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdexInput_csv import ClimdexInputCSV


def build_params(
    tmax_file,
    tmin_file,
    prec_file,
    tmax_column,
    tmin_column,
    prec_column,
    base_range,
    vector_name,
    output_file,
):
    return (
        f"tmax_file=@xlink:href={tmax_file};"
        f"tmin_file=@xlink:href={tmin_file};"
        f"prec_file=@xlink:href={prec_file};"
        f"tmax_column={tmax_column};"
        f"tmin_column={tmin_column};"
        f"prec_column={prec_column};"
        f"base_range={base_range};"
        f"out_file={output_file};"
        f"vector_name={vector_name};"
    )


@pytest.mark.parametrize(
    (
        "tmax_file",
        "tmin_file",
        "prec_file",
        "tmax_column",
        "tmin_column",
        "prec_column",
        "base_range",
        "vector_name",
    ),
    [
        (
            local_path("1018935_MAX_TEMP.csv"),
            local_path("1018935_MIN_TEMP.csv"),
            local_path("1018935_ONE_DAY_PRECIPITATION.csv"),
            "MAX_TEMP",
            "MIN_TEMP",
            "ONE_DAY_PRECIPITATION",
            "c(1971, 2000)",
            "climdexInput",
        ),
    ],
)
def test_wps_climdexInput_csv(
    tmax_file,
    tmin_file,
    prec_file,
    tmax_column,
    tmin_column,
    prec_column,
    base_range,
    vector_name,
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            tmax_file,
            tmin_file,
            prec_file,
            tmax_column,
            tmin_column,
            prec_column,
            base_range,
            vector_name,
            out_file.name,
        )
        run_wps_process(ClimdexInputCSV(), datainputs)


@pytest.mark.parametrize(
    (
        "tmax_file",
        "tmin_file",
        "prec_file",
        "tmax_column",
        "tmin_column",
        "prec_column",
        "base_range",
        "vector_name",
    ),
    [
        (
            local_path("1018935_MAX_TEMP.csv"),
            local_path("1018935_MIN_TEMP.csv"),
            local_path("1018935_ONE_DAY_PRECIPITATION.csv"),
            "FAKE_COLUMN",
            "MIN_TEMP",
            "ONE_DAY_PRECIPITATION",
            "c(1971, 2000)",
            "climdexInput",
        ),
    ],
)
def test_wps_climdexInput_csv_column_err(
    tmax_file,
    tmin_file,
    prec_file,
    tmax_column,
    tmin_column,
    prec_column,
    base_range,
    vector_name,
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            tmax_file,
            tmin_file,
            prec_file,
            tmax_column,
            tmin_column,
            prec_column,
            base_range,
            vector_name,
            out_file.name,
        )
        process_err_test(ClimdexInputCSV, datainputs)


@pytest.mark.parametrize(
    (
        "tmax_file",
        "tmin_file",
        "prec_file",
        "tmax_column",
        "tmin_column",
        "prec_column",
        "base_range",
        "vector_name",
    ),
    [
        (
            local_path("1018935_MAX_TEMP.csv"),
            local_path("1018935_MIN_TEMP.csv"),
            local_path("1018935_ONE_DAY_PRECIPITATION.csv"),
            "FAKE_COLUMN",
            "MIN_TEMP",
            "ONE_DAY_PRECIPITATION",
            "c1971, 2000)",
            "climdexInput",
        ),
    ],
)
def test_wps_climdexInput_csv_syntax_err(
    tmax_file,
    tmin_file,
    prec_file,
    tmax_column,
    tmin_column,
    prec_column,
    base_range,
    vector_name,
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            tmax_file,
            tmin_file,
            prec_file,
            tmax_column,
            tmin_column,
            prec_column,
            base_range,
            vector_name,
            out_file.name,
        )
        process_err_test(ClimdexInputCSV, datainputs)
