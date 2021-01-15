import pytest, logging, requests, io
from rpy2 import robjects
from pywps import Service, tests
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib.embedded import RRuntimeError
from urllib.request import urlretrieve
from pkg_resources import resource_filename
from tempfile import NamedTemporaryFile
from contextlib import redirect_stderr

from wps_tools.output_handling import rda_to_vector, load_rdata_to_python
from wps_tools.testing import run_wps_process


logger = logging.getLogger("PYWPS")
logger.setLevel(logging.NOTSET)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: quail: %(message)s", "%Y-%m-%d %H:%M:%S"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def collect_literal_inputs(request):
    literal_inputs = [
        request.inputs[k][0].data
        for k in request.inputs.keys()
        if "data_type" in vars(request.inputs[k][0]).keys()
    ]
    return literal_inputs


def load_ci(climdex_input, ci_name):
    try:
        ci = load_rdata_to_python(climdex_input, ci_name)
        if ci.rclass[0] == "climdexInput":
            return ci
        else:
            raise ProcessError(
                msg="Input for ci-name is not a valid climdexInput object"
            )

    except RRuntimeError:
        logger.error(f"cannot load {ci_name} from {climdex_input}")
        raise ProcessError(
            msg="Either your file is not a valid Rdata file or the climdexInput object name is not found in this rda file"
        )


def load_rda(file_, obj_name):
    try:
        return load_rdata_to_python(file_, obj_name)
    except RRuntimeError:
        raise ProcessError(
            msg="Either your file is not a valid Rdata file or there is no object of that name is not found in this rda file"
        )


# Teting functions

def test_rda_output(url, vector_name, expected_file, expected_vector_name):
    output_vector = rda_to_vector(url, vector_name)
    local_path = resource_filename("tests", f"data/{expected_file}")
    expected_url = f"file://{local_path}"
    expected_vector = rda_to_vector(expected_url, expected_vector_name)

    for index in range(len(expected_vector)):
        assert str(output_vector[index]) == str(expected_vector[index])

    # Clear R global env
    robjects.r("rm(list=ls())")


def test_ci_output(url, vector_name, expected_file, expected_vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True
    ) as tmp_file:
        urlretrieve(url, tmp_file.name)
        robjects.r(f"load(file='{tmp_file.name}')")

    slots = [
        "data",
        "namasks",
        "dates",
        "jdays",
        "base.range",
        "date.factors",
        "northern.hemisphere",
        "max.missing.days",
    ]

    for slot in slots:
        output_slot = robjects.r(f"{vector_name}@{slot}")

        robjects.r(
            "load(file='{}')".format(
                resource_filename("tests", f"data/{expected_file}")
            )
        )
        expected_slot = robjects.r(f"{expected_vector_name}@{slot}")

        for index in range(len(expected_slot)):
            assert str(output_slot[index]) == str(expected_slot[index])

    # Clear R global env
    robjects.r("rm(list=ls())")


def process_err_test(process, datainputs, err_type):
    err = io.StringIO()
    with redirect_stderr(err):
        with pytest.raises(Exception):
            run_wps_process(process(), datainputs)

    if err_type == "unknown ci name":
        msg = "Either your file is not a valid Rdata file or the climdexInput object name is not found in this rda file"
    if err_type == "class is not ci":
        msg = "Input for ci-name is not a valid climdexInput object"
    assert msg in err.getvalue()