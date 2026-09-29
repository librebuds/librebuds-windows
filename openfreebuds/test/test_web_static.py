"""LibreBuds: the page served at GET / shows the LibreBuds name."""
from openfreebuds.webserver import STATIC_PATH


def test_index_title():
    html = (STATIC_PATH / "index.html").read_text(encoding="utf-8")
    assert "<title>LibreBuds RPC</title>" in html
    assert "LibreBuds RPC" in html.split("<h2>", 1)[1].split("</h2>", 1)[0]
    assert "OpenFreebuds RPC" not in html
