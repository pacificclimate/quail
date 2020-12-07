from .wps_climdex_days import ClimdexDays
from .wps_climdex_gsl import ClimdexGSL

processes = [
    ClimdexDays(),
    ClimdexGSL(),
]
