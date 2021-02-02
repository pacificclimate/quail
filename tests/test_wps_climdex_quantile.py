import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path, process_err_test
from quail.processes.wps_climdex_quantile import ClimdexQuantile


def build_params(
    data_vector,
    quantiles_vector,
    vector_name,
    output_file,
    data_rda=None,
    data_rds=None,
):
    params = (
        f"data_vector={data_vector};"
        f"quantiles_vector={quantiles_vector};"
        f"vector_name={vector_name};"
        f"output_file={output_file};"
    )
    if data_rda:
        return params + f"data_rda=@xlink:href={data_rda};"
    elif data_rds:
        return params + f"data_rds=@xlink:href={data_rds};"
    else:
        return params


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
            data_vector,
            quantiles_vector,
            vector_name,
            out_file.name,
            data_rda=data_file,
        )
        run_wps_process(ClimdexQuantile(), datainputs)


@pytest.mark.parametrize(
    (
        "data_file",
        "data_vector",
        "quantiles_vector",
        "vector_name",
    ),
    [
        (
            local_path("ec.1018935.rds"),
            "unlist(ec.1018935.tmax['MAX_TEMP'])",
            "c(0.1, 0.5, 0.9)",
            "tmax_quantiles",
        ),
    ],
)
def test_wps_climdex_quantile_rds(
    data_file,
    data_vector,
    quantiles_vector,
    vector_name,
):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = build_params(
            data_vector,
            quantiles_vector,
            vector_name,
            out_file.name,
            data_rds=data_file,
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
            data_vector,
            quantiles_vector,
            vector_name,
            out_file.name,
            data_rda=data_file,
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
            data_vector,
            quantiles_vector,
            vector_name,
            out_file.name,
            data_rda=data_file,
        )
        process_err_test(ClimdexQuantile, datainputs)
