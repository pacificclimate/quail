from .wps_climdex_days import ClimdexDays
from .wps_climdexInput_csv import ClimdexInputCSV
from .wps_climdexInput_raw import ClimdexInputRaw

processes = [
    ClimdexDays(),
    ClimdexInputCSV(),
    ClimdexInputRaw(),
]
