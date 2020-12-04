from .wps_climdex_fd import ClimdexFD
from .wps_climdex_su import ClimdexSU

processes = [
    ClimdexFD(),
    ClimdexSU(),
]
