from .wps_climdex_days import ClimdexDays
from .wps_climdexInput import ClimdexInput

processes = [
    ClimdexDays(),
    ClimdexInput(),
]
