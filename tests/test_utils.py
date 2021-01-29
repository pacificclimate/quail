import pytest
import io
from pkg_resources import resource_filename
from pywps.app.exceptions import ProcessError
from tempfile import NamedTemporaryFile
from contextlib import redirect_stderr

from quail.utils import load_ci, load_rda, validate_vector
from wps_tools.testing import local_path


@pytest.mark.parametrize(
    ("file_", "obj_name"),
    [
        (resource_filename("tests", "data/expected_gsl.rda"), "expected_gsl_vector"),
    ],
)
def test_load_ci_obj_err(file_, obj_name):
    with pytest.raises(ProcessError) as e:
        load_ci(file_, obj_name)
    assert (
        str(vars(e)["_excinfo"][1])
        == "Input for ci-name is not a valid climdexInput object"
    )


@pytest.mark.parametrize(
    ("file_", "obj_name"),
    [
        (resource_filename("tests", "data/climdexInput.rda"), "not_ci"),
    ],
)
def test_load_ci_name_err(file_, obj_name):
    with pytest.raises(ProcessError) as e:
        load_ci(file_, obj_name)
    assert (
        str(vars(e)["_excinfo"][1])
        == "RRuntimeError: The variable name passed is not an object found in the given rda file"
    )


@pytest.mark.parametrize(
    ("file_", "obj_name"),
    [
        (resource_filename("tests", "data/expected_days_data.rda"), "autumn_days"),
    ],
)
def test_load_rda_err(file_, obj_name):
    with pytest.raises(ProcessError) as e:
        load_rda(file_, obj_name)
        assert (
            str(vars(e)["_excinfo"][1])
            == "RRuntimeError: One of the variable names passed is not an object found in the given rda files"
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
