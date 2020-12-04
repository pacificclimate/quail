from .wps_say_hello import SayHello
from .wps_climdex_fd import ClimdexFD
from .wps_climdex_su import ClimdexSU

processes = [
    SayHello(),
    ClimdexFD(),
    ClimdexSU(),
]
