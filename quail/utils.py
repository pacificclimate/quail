import pytest, logging, requests, io, re
from rpy2 import robjects
from pywps import Service, tests
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib._rinterface_capi import RParsingError
from rpy2.rinterface_lib.embedded import RRuntimeError
from urllib.request import urlretrieve
from pkg_resources import resource_filename
from tempfile import NamedTemporaryFile
from contextlib import redirect_stderr

from wps_tools.output_handling import rda_to_vector, load_rdata_to_python
from wps_tools.testing import run_wps_process
from wps_tools.R import get_package

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


def validate_vector(vector):
    try:
        robjects.r(vector)
    except RParsingError:
        raise ProcessError(
            "RRuntimeError: Invalid vector format, follow R vector syntax"
        )


def load_ci(climdex_input, ci_name):
    try:
        ci = load_rdata_to_python(climdex_input, ci_name)
        if ci.rclass[0] == "climdexInput":
            return ci
        else:
            raise ProcessError(
                msg="RRuntimeError: Input for ci-name is not a valid climdexInput object"
            )

    except RRuntimeError:
        logger.error(f"cannot load {ci_name} from {climdex_input}")
        raise ProcessError(
            msg="RRuntimeError: Either your file is not a valid Rdata file or the climdexInput object name is not found in this rda file"
        )


def load_rda(file_, obj_name):
    try:
        return load_rdata_to_python(file_, obj_name)
    except RRuntimeError as e:
        err_name = re.compile(r"object \'(.*)\' not found").findall(str(e))
        if "_" in err_name[0]:
            raise ProcessError(
                msg=f"RRuntimeError: One of the variable names passed is not an object found in the given rda files"
            )
        else:
            raise ProcessError(
                msg=f"RRuntimeError: There is no object named {err_name[0]} in this rda file"
            )


def r_valid_name(robj_name):
    """The R function 'make.names' will change a name if it
    is not syntactically correct and leave it if it is
    """
    base = get_package("base")
    if base.make_names(robj_name)[0] != robj_name:
        raise ProcessError(msg="RRuntimeError: Your vector name is not a valid R name")


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
        msg = "RRuntimeError: Either your file is not a valid Rdata file or the climdexInput object name is not found in this rda file"
    elif err_type == "class is not ci":
        msg = "RRuntimeError: Input for ci-name is not a valid climdexInput object"
    elif err_type == "load_rda err":
        msg = "object"
    elif err_type == "invalid vector name":
        msg = "RRuntimeError: Your vector name is not a valid R name"
    assert msg in err.getvalue()
