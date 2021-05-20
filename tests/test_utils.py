import pytest
from pkg_resources import resource_filename
from pywps.app.exceptions import ProcessError

from quail.utils import (
    get_ClimdexInputs,
    load_rds_ci,
    load_cis,
    validate_vectors,
)


@pytest.mark.parametrize(
    ("r_file"),
    [
        resource_filename("tests", "data/climdexInput.rda"),
        resource_filename("tests", "data/climdex_input_multiple.rda"),
    ],
)
def test_get_ClimdexInputs(r_file):
    cis = get_ClimdexInputs(r_file)
    assert len(cis) > 0
    for ci in cis.values():
        assert ci.rclass[0] == "climdexInput"


@pytest.mark.parametrize(
    ("r_file"),
    [
        resource_filename("tests", "data/expected_days_data.rda"),
        resource_filename("tests", "data/expected_gsl.rda"),
    ],
)
def test_get_ClimdexInputs_err(r_file):
    with pytest.raises(IndexError):
        cis = get_ClimdexInputs(r_file)


@pytest.mark.parametrize(
    ("r_file"),
    [
        resource_filename("tests", "data/climdexInput.rds"),
    ],
)
def test_load_rds_ci(r_file):
    ci = load_rds_ci(r_file)
    assert ci.rclass[0] == "climdexInput"


@pytest.mark.parametrize(
    ("r_file"),
    [
        resource_filename("tests", "data/climdexInput.rda"),
        resource_filename("tests", "data/climdexInput.rds"),
        resource_filename("tests", "data/climdex_input_multiple.rda"),
    ],
)
def test_load_cis(r_file):
    cis = load_cis(r_file)
    assert len(cis) > 0
    for ci in cis.values():
        assert ci.rclass[0] == "climdexInput"


@pytest.mark.parametrize(
    ("r_file"),
    [
        resource_filename("tests", "data/expected_days_data.rda"),
        resource_filename("tests", "data/1018935_MAX_TEMP.csv"),
    ],
)
def test_load_cis_err(r_file):
    with pytest.raises(ProcessError) as e:
        load_cis(r_file)
    assert (
        str(vars(e)["_excinfo"][1]) == "RRuntimeError: Data file must be a RDS file or "
        "a Rdata file containing a ClimdexInput object of the given name"
    )


@pytest.mark.parametrize(
    ("vectors"),
    [[("c('cats')"), ("c('cats', 'dogs')"), ("c(cats=1, dogs=2)")]],
)
def test_validate_vectors(vectors):
    validate_vectors(vectors)


@pytest.mark.parametrize(
    ("vectors"),
    [[("()")], [("c'cats', 'dogs')")]],
)
def test_validate_vectors_err(vectors):
    with pytest.raises(ProcessError) as e:
        validate_vectors(vectors)
    assert (
        str(vars(e)["_excinfo"][1])
        == "RParsingError: Invalid vector format, follow R vector syntax"
    )
