import pytest
import sys
from rpy2 import robjects
from itertools import chain
from tempfile import NamedTemporaryFile

from wps_tools.testing import run_wps_process, local_path
from quail.processes.wps_climdex_get_available_indices import GetIndices
from quail.utils import process_err_test


@pytest.mark.parametrize(
    ("climdex_input", "ci_name"),
    [(local_path("climdexInput.rda"), "ci")],
)
def test_wps_get_available_indices(climdex_input, ci_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"output_file={out_file.name};"
        )
        run_wps_process(GetIndices(), datainputs)


@pytest.mark.parametrize(
    ("climdex_input", "ci_name", "err_type"),
    [
        (local_path("climdexInput.rda"), "not_ci", "unknown ci name"),
        (local_path("expected_dtr.rda"), "expected_dtr_annual", "class is not ci"),
    ],
)
def test_wps_get_available_indices_err(climdex_input, ci_name, err_type):
    with NamedTemporaryFile(
        suffix=".rda", prefix="output_", dir="/tmp", delete=True
    ) as out_file:
        datainputs = (
            f"climdex_input=@xlink:href={climdex_input};"
            f"ci_name={ci_name};"
            f"output_file={out_file.name};"
        )
        process_err_test(GetIndices, datainputs, err_type)


@pytest.mark.parametrize(
    ("avail_indices"),
    [
        (["su", "txx", "tnx", "dtr", "r95ptot"]),
        (robjects.r("c(c('sdii'), c('fd'), c('prcptot'), c('wsdi'))")),
    ],
)
def test_available_processes(avail_indices):
    process = GetIndices()
    avail_processes = process.available_processes(avail_indices)
    values = list(chain.from_iterable(avail_processes.values()))

    assert len(avail_indices) == len(values)

    for index in avail_indices:
        assert index in values
