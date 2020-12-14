import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdexInput_raw import ClimdexInputRaw


@pytest.mark.parametrize(
    (
        "tmax_file",
        "tmin_file",
        "prec_file",
        "tmax_name",
        "tmin_name",
        "prec_name",
        "tmax_column",
        "tmin_column",
        "prec_column",
        "base_range",
        "vector_name",
    ),
    [
        (
            local_path("ec.1018935.rda"),
            local_path("ec.1018935.rda"),
            local_path("ec.1018935.rda"),
            "ec.1018935.tmax",
            "ec.1018935.tmin",
            "ec.1018935.prec",
            "MAX_TEMP",
            "MIN_TEMP",
            "ONE_DAY_PRECIPITATION",
            "c(1971, 2000)",
            "climdexInput",
        ),
    ],
)
def test_wps_climdexInput_raw(
    tmax_file,
    tmin_file,
    prec_file,
    tmax_name,
    tmin_name,
    prec_name,
    tmax_column,
    tmin_column,
    prec_column,
    base_range,
    vector_name,
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"tmax_file=@xlink:href={tmax_file};"
            f"tmin_file=@xlink:href={tmin_file};"
            f"prec_file=@xlink:href={prec_file};"
            f"tmax_name={tmax_name};"
            f"tmin_name={tmin_name};"
            f"prec_name={prec_name};"
            f"tmax_column={tmax_column};"
            f"tmin_column={tmin_column};"
            f"prec_column={prec_column};"
            f"base_range={base_range};"
            f"out_file={out_file.name};"
            f"vector_name={vector_name};"
        )
        run_wps_process(ClimdexInputRaw(), datainputs)
