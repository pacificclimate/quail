import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_quantile import ClimdexQuantile


def build_params(data_file, data_vector, quantiles_vector, vector_name, output_file):
    return (
        f"data_file=@xlink:href={data_file};"
        f"data_vector={data_vector};"
        f"quantiles_vector={quantiles_vector};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )


@pytest.mark.parametrize(
    (
        "data_file",
        "data_vector",
        "quantiles_vector",
        "vector_name",
    ),
    [
        (
            local_path("ec.1018935.rda"),
            "unlist(ec.1018935.tmax['MAX_TEMP'])",
            "c(0.1, 0.5, 0.9)",
            "tmax_quantiles",
        ),
        (
            None,
            "0:10",
            "0.5",
            "quantile_50p",
        ),
    ],
)
def test_wps_climdex_quantile(
    data_file,
    data_vector,
    quantiles_vector,
    vector_name,
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            data_file, data_vector, quantiles_vector, vector_name, out_file.name
        )
        run_wps_process(ClimdexQuantile(), datainputs)


@pytest.mark.parametrize(
    ("data_file", "data_vector", "quantiles_vector", "vector_name"),
    [
        (
            local_path("ec.1018935.rda"),
            "not_tmax",
            "c(0.1, 0.5, 0.9)",
            "tmax quantiles",
        ),
        (
            local_path("ec.1018935.rda"),
            "not_tmax",
            "c0.1, 0.5, 0.9)",
            "tmax_quantiles",
        ),
    ],
)
def test_wps_climdex_quantile_vector_err(
    data_file, data_vector, quantiles_vector, vector_name
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            data_file, data_vector, quantiles_vector, vector_name, out_file.name
        )
        process_err_test(ClimdexQuantile, datainputs)


@pytest.mark.parametrize(
    ("data_file", "data_vector", "quantiles_vector", "vector_name"),
    [
        (
            local_path("ec.1018935.rda"),
            "not_tmax",
            "c(0.1, 0.5, 0.9)",
            "tmax_quantiles",
        ),
    ],
)
def test_wps_climdex_quantile_load_rda__err(
    data_file, data_vector, quantiles_vector, vector_name
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            data_file, data_vector, quantiles_vector, vector_name, out_file.name
        )
        process_err_test(ClimdexQuantile, datainputs)
