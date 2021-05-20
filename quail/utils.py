import logging
from rpy2 import robjects
from pywps.app.exceptions import ProcessError
from rpy2.rinterface_lib._rinterface_capi import RParsingError
from rpy2.rinterface_lib.embedded import RRuntimeError

# Libraries for test functions
from urllib.request import urlretrieve
from pkg_resources import resource_filename
from tempfile import NamedTemporaryFile

# PCIC libraries
from wps_tools.R import get_robjects, load_rdata_to_python
from wps_tools.io import collect_args


logger = logging.getLogger("PYWPS")
logger.setLevel(logging.NOTSET)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: quail: %(message)s", "%Y-%m-%d %H:%M:%S"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def validate_vectors(vectors):
    for vector in vectors:
        try:
            vect = robjects.r(vector)
            if not robjects.r["is.vector"](vect)[0]:
                raise ProcessError("Invalid type passed for vector")

        except RParsingError as e:
            raise ProcessError(
                msg=f"{type(e).__name__}: Invalid vector format, follow R vector syntax"
            )


def get_ClimdexInputs(r_file):
    """Returns a dictionary of all ClimdexInput Objects from an Rdata file."""
    robjs = list(robjects.r(f"load(file='{r_file}')"))
    cis = {
        ci: robjects.r(ci) for ci in robjs if robjects.r(ci).rclass[0] == "climdexInput"
    }
    if len(cis) == 0:
        raise IndexError
    else:
        return cis


def load_cis(r_file):
    """RDS and RDA files have the same mimetype, so the pyWPS ClimdexInput
    is unable to tell them apart and apply the correct suffix. The R function
    `load()` can only read Rdata files and `readRDS()` can only read RDS
    files. Without the input having a suffix, this function passes the input
    to `load()`, then, if that raises an exception, passes it to `readRDS()`,
    and finally if that fails, raises a ProcessError.
    """
    try:
        return get_ClimdexInputs(r_file)
    except (RRuntimeError, ProcessError, IndexError):
        pass

    try:
        return {"ci": load_rds_ci(r_file)}
    except (RRuntimeError, ProcessError) as e:
        raise ProcessError(
            f"{type(e).__name__}: Data file must be a RDS file or "
            "a Rdata file containing a ClimdexInput object of the given name"
        )


def load_rds_ci(r_file):
    """Loads an object from an RDS file and checks that is a ClimdexInput object"""
    ci = robjects.r(f"readRDS('{r_file}')")
    if ci.rclass[0] == "climdexInput":
        return ci
    else:
        raise ProcessError


def get_robj(r_file, object_name):
    """RDS and RDA files have the same mimetype, so the pyWPS ClimdexInput
    is unable to tell them apart and apply the correct suffix. The R function
    `load()` can only read Rdata files and `readRDS()` can only read RDS
    files. Without the input having a suffix, this function passes the input
    to `load()`, then, if that raises an exception, passes it to `readRDS()`,
    and finally if that fails, raises a ProcessError.
    """
    try:
        return load_rdata_to_python(r_file, object_name)
    except (RRuntimeError, ProcessError, IndexError):
        pass

    try:
        return robjects.r(f"readRDS('{r_file}')")
    except (RRuntimeError, ProcessError) as e:
        raise ProcessError(
            f"{type(e).__name__}: Data file must be a RDS file or "
            "a Rdata file containing an object of the given name"
        )


# Testing


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
