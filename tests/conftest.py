import pytest
from pkg_resources import resource_filename
from wps_tools.file_handling import csv_handler


@pytest.fixture
def tmax_file_content():
    return csv_handler(resource_filename("tests", "data/1018935_MAX_TEMP.csv"))


@pytest.fixture
def tmin_file_content():
    return csv_handler(resource_filename("tests", "data/1018935_MIN_TEMP.csv"))


@pytest.fixture
def prec_file_content():
    return csv_handler(
        resource_filename("tests", "data/1018935_ONE_DAY_PRECIPITATION.csv")
    )
