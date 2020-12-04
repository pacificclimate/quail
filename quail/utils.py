import logging
from rpy2.robjects.packages import isinstalled, importr
from rpy2 import robjects
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


def load_rdata(input_file, obj_name):
    robjects.r(f"load(file='{input_file}')")
    return robjects.r(obj_name)


def save_rdata(obj_name, obj, output_path, workdir):
    robjects.r.assign(obj_name, obj)
    robjects.r(f"save({obj_name}, file='{output_path}')")
