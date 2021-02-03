import pytest
from pkg_resources import resource_filename
from pywps.app.exceptions import ProcessError

from quail.utils import load_ci, validate_vector


@pytest.mark.parametrize(
    ("args", "obj_name"),
    [
        (
            {"ci_rda": [resource_filename("tests", "data/expected_gsl.rda")]},
            "expected_gsl_vector",
        ),
    ],
)
def test_load_ci_obj_err(args, obj_name):
    with pytest.raises(ProcessError) as e:
        load_ci(args, obj_name)
    assert (
        str(vars(e)["_excinfo"][1])
        == "Input for ci-name is not a valid climdexInput object"
    )


@pytest.mark.parametrize(
    ("args", "obj_name"),
    [({"ci_rda": [resource_filename("tests", "data/climdexInput.rda")]}, "not_ci"),],
)
def test_load_ci_name_err(args, obj_name):
    with pytest.raises(ProcessError) as e:
        load_ci(args, obj_name)
    assert (
        str(vars(e)["_excinfo"][1])
        == "RRuntimeError: The variable name passed is not an object found in the given rda file"
    )


@pytest.mark.parametrize(
    ("args", "obj_name"),
    [({"not_ci": [resource_filename("tests", "data/climdexInput.rda")]}, "ci"),],
)
def test_load_ci_args_err(args, obj_name):
    with pytest.raises(ProcessError) as e:
        load_ci(args, obj_name)
    assert (
        str(vars(e)["_excinfo"][1])
        == "You must provide either a Rda or RDS file containing the climdexInput"
    )


@pytest.mark.parametrize(
    ("vector"), [("c('cats')"), ("c('cats', 'dogs')"), ("c(cats=1, dogs=2)")],
)
def test_validate_vector(vector):
    validate_vector(vector)


@pytest.mark.parametrize(
    ("vector"), [("()"), ("c'cats', 'dogs')")],
)
def test_validate_vector_err(vector):
    with pytest.raises(ProcessError) as e:
        validate_vector(vector)
    assert (
        str(vars(e)["_excinfo"][1])
        == "RParsingError: Invalid vector format, follow R vector syntax"
    )
