from pywps import Service

from .common import client_for
from quail.processes import processes


def test_wps_caps():
    client = client_for(Service(processes=processes))
    resp = client.get(service="wps", request="getcapabilities", version="1.0.0")
    names = resp.xpath_text(
        "/wps:Capabilities" "/wps:ProcessOfferings" "/wps:Process" "/ows:Identifier"
    )
    assert sorted(names.split()) == [
        "climdex_days",
        "climdex_gsl",
        "climdex_input_csv",
        "climdex_input_raw",
        "climdex_mmdmt",
        "climdex_spells",
        "climdex_temp_pctl",
    ]
