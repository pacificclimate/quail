from .wps_climdex_su import ClimdexSU
from .wps_climdex_id import ClimdexID

processes = [
    ClimdexSU(),
    ClimdexID(),
]
