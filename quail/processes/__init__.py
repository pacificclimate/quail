from .wps_climdex_days import ClimdexDays
from .wps_climdex_gsl import ClimdexGSL
from .wps_climdexInput_csv import ClimdexInputCSV
from .wps_climdexInput_raw import ClimdexInputRaw
from .wps_climdex_mmdmt import ClimdexMMDMT
from .wps_climdex_rmm import ClimdexRMM
from .wps_climdex_spells import ClimdexSpells
from .wps_climdex_temp_pctl import ClimdexTempPctl

processes = [
    ClimdexDays(),
    ClimdexGSL(),
    ClimdexInputCSV(),
    ClimdexInputRaw(),
    ClimdexMMDMT(),
    ClimdexRMM(),
    ClimdexSpells(),
    ClimdexTempPctl(),
]
