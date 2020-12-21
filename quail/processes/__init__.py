from .wps_climdex_days import ClimdexDays
from .wps_climdex_gsl import ClimdexGSL
from .wps_climdexInput_csv import ClimdexInputCSV
from .wps_climdexInput_raw import ClimdexInputRaw
from .wps_climdex_mmdmt import ClimdexMMDMT
from .wps_climdex_rmm import ClimdexRMM
from .wps_climdex_spells import ClimdexSpells
from .wps_climdex_temp_pctl import ClimdexTempPctl
from .wps_climdex_get_available_indices import ClimdexGetAvailableIndices
from .wps_climdex_dtr import ClimdexDTR
from .wps_climdex_ptot import ClimdexPtot
from .wps_climdex_quantile import ClimdexQuantile
from .wps_climdex_sdii import ClimdexSDII
from .wps_climdex_rxnday import ClimdexRxnday

processes = [
    ClimdexDays(),
    ClimdexGSL(),
    ClimdexInputCSV(),
    ClimdexInputRaw(),
    ClimdexMMDMT(),
    ClimdexRMM(),
    ClimdexSpells(),
    ClimdexTempPctl(),
    ClimdexGetAvailableIndices(),
    ClimdexDTR(),
    ClimdexPtot(),
    ClimdexQuantile(),
    ClimdexSDII(),
    ClimdexRxnday(),
]
