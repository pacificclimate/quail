import pytest
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_quantile import ClimdexQuantile


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
        datainputs = (
            f"data_file=@xlink:href={data_file};"
            f"data_vector={data_vector};"
            f"quantiles_vector={quantiles_vector};"
            f"vector_name={vector_name};"
            f"output_file={out_file.name};"
        )

        run_wps_process(ClimdexQuantile(), datainputs)
