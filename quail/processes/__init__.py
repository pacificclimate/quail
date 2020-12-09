from .wps_climdex_days import ClimdexDays
from .wps_climdexInput_raw import ClimdexInputRaw

processes = [
    ClimdexDays(),
    ClimdexInputRaw(),
]
