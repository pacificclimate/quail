from .wps_say_hello import SayHello
from .wps_climdex_fd import ClimdexFD

processes = [
    SayHello(),
    ClimdexFD(),
]
