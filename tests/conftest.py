import pytest
from importlib.resources import files
from wps_tools.file_handling import csv_handler


@pytest.fixture
def tmax_file_content():
    return csv_handler((files("tests") / "data/1018935_MAX_TEMP.csv"))


@pytest.fixture
def tmin_file_content():
    return csv_handler((files("tests") / "data/1018935_MIN_TEMP.csv"))


@pytest.fixture
def prec_file_content():
    return csv_handler((files("tests") / "data/1018935_ONE_DAY_PRECIPITATION.csv"))
