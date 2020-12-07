import logging
from rpy2 import robjects
from rpy2.robjects.packages import isinstalled, importr
from pywps.app.exceptions import ProcessError
from urllib.request import urlretrieve
from pkg_resources import resource_filename
from tempfile import NamedTemporaryFile

logger = logging.getLogger("PYWPS")
logger.setLevel(logging.NOTSET)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: quail: %(message)s", "%Y-%m-%d %H:%M:%S"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_package(package):
    if isinstalled(package):
        return importr(package)
    else:
        raise ProcessError(f"R package, {package}, is not installed")


def load_rdata_to_python(r_file, r_object_name):
    robjects.r(f"load(file='{r_file}')")
    return robjects.r(r_object_name)


def save_python_to_rdata(r_name, py_var, r_file):
    robjects.r.assign(r_name, py_var)
    robjects.r(f"save({r_name}, file='{r_file}')")


def test_rda_output(url, vector_name, expected_file, expected_vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True
    ) as tmp_file:
        urlretrieve(url, tmp_file.name)
        robjects.r(f"load(file='{tmp_file.name}')")

    output_vector = robjects.r(vector_name)

    robjects.r(
        "load(file='{}')".format(resource_filename("tests", f"data/{expected_file}"))
    )
    expected_vector = robjects.r(expected_vector_name)

    for index in range(len(expected_vector)):
        assert str(output_vector[index]) == str(expected_vector[index])
