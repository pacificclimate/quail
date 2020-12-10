from .wps_climdex_days import ClimdexDays
from .wps_climdex_gsl import ClimdexGSL
from .wps_climdex_mmdmt import ClimdexMMDMT
from .wps_climdex_sdi import ClimdexSDI

processes = [
    ClimdexDays(),
    ClimdexGSL(),
    ClimdexMMDMT(),
    ClimdexSDI(),
]
