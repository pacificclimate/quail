import pytest
from pkg_resources import resource_filename
from pywps.app.exceptions import ProcessError

from quail.utils import load_ci, validate_vector


@pytest.mark.parametrize(
    ("r_file", "ci_name"),
    [
        (resource_filename("tests", "data/climdexInput.rda"), "ci"),
        (resource_filename("tests", "data/climdexInput.rds"), "ci"),
    ],
)
def test_load_ci(r_file, ci_name):
    ci = load_ci(r_file, ci_name)
    assert ci.rclass[0] == "climdexInput"


@pytest.mark.parametrize(
    ("r_file", "ci_name"),
    [
        (
            resource_filename("tests", "data/expected_gsl.rda"),
            "expected_gsl_vector",
        ),
    ],
)
def test_load_ci_obj_err(r_file, ci_name):
    with pytest.raises(ProcessError) as e:
        load_ci(r_file, ci_name)
    assert (
        str(vars(e)["_excinfo"][1])
        == "Input for ci-name is not a valid climdexInput object"
    )


@pytest.mark.parametrize(
    ("r_file", "ci_name"),
    [
        (resource_filename("tests", "data/climdexInput.rda"), "not_ci"),
        (resource_filename("tests", "data/1018935_MAX_TEMP.csv"), "ci"),
    ],
)
def test_load_file_err(r_file, ci_name):
    with pytest.raises(ProcessError) as e:
        load_ci(r_file, ci_name)
    assert (
        str(vars(e)["_excinfo"][1]) == "RRuntimeError: Data file must be a RDS file or "
        "a Rdata file containing an object of the given name"
    )


@pytest.mark.parametrize(
    ("vector"),
    [("c('cats')"), ("c('cats', 'dogs')"), ("c(cats=1, dogs=2)")],
)
def test_validate_vector(vector):
    validate_vector(vector)


@pytest.mark.parametrize(
    ("vector"),
    [("()"), ("c'cats', 'dogs')")],
)
def test_validate_vector_err(vector):
    with pytest.raises(ProcessError) as e:
        validate_vector(vector)
    assert (
        str(vars(e)["_excinfo"][1])
        == "RParsingError: Invalid vector format, follow R vector syntax"
    )
