from .wps_climdex_days import ClimdexDays
from .wps_climdex_gsl import ClimdexGSL
from .wps_climdex_mmdmt import ClimdexMMDMT

processes = [
    ClimdexDays(),
    ClimdexGSL(),
    ClimdexMMDMT(),
]
