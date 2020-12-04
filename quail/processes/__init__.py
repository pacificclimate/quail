from .wps_climdex_su import ClimdexSU
from .wps_climdex_id import ClimdexID
from .wps_climdex_days import ClimdexDays

processes = [
    ClimdexDays(),
    ClimdexSU(),
    ClimdexID(),
]
