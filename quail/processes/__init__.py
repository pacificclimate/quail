from .wps_climdex_days import ClimdexDays
from .wps_climdex_gsl import ClimdexGSL
from .wps_climdexInput_raw import ClimdexInputRaw


processes = [
    ClimdexDays(),
    ClimdexGSL(),
    ClimdexInputRaw(),
]
