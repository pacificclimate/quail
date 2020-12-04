import logging
from rpy2 import robjects
from rpy2.robjects.packages import isinstalled, importr
from pywps.app.exceptions import ProcessError


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