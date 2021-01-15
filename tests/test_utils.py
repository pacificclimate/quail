import pytest
import io
from pywps.app.exceptions import ProcessError
from tempfile import NamedTemporaryFile
from contextlib import redirect_stderr

from quail.utils import load_ci, load_rda
from wps_tools.testing import local_path


@pytest.mark.parametrize(
    ("file_", "obj_name"),
    [
        (local_path("expected_days_data.rda"), "summer_days"),
    ],
)
def test_load_ci_obj_err(file_, obj_name):
    with pytest.raises(ProcessError) as e:
        load_ci(file_, obj_name)
        assert str(vars(e)["_excinfo"][1]) == "Input for ci-name is not a valid climdexInput object"


@pytest.mark.parametrize(
    ("file_", "obj_name"),
    [
        (local_path("climdexInput.rda"), "not_ci"),
    ],
)
def test_load_ci_name_err(file_, obj_name):
    with pytest.raises(ProcessError) as e:
        load_ci(file_, obj_name)
        assert str(vars(e)["_excinfo"][1]) == "Either your file is not a valid Rdata file or the climdexInput object name is not found in this rda file"


@pytest.mark.parametrize(
    ("file_", "obj_name"),
    [
        (local_path("expected_days_data.rda"), "autumn_days"),
    ],
)
def test_load_rda_err(file_, obj_name):
    with pytest.raises(ProcessError) as e:
        load_rda(file_, obj_name)
        assert str(vars(e)["_excinfo"][1]) == "Either your file is not a valid Rdata file or there is no object of that name is not found in this rda file"