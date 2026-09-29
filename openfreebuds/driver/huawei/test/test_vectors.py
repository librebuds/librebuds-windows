"""Replays the shared LibreBuds test vectors through the upstream packet parser."""
import json
import pathlib

import pytest

from openfreebuds.driver.huawei.package import HuaweiSppPackage

VECTOR_ROOT = pathlib.Path(__file__).resolve().parents[4] / "vendor" / "librebuds" / "test-vectors"


def load_vectors():
    vectors = []
    for path in sorted(VECTOR_ROOT.rglob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                vectors.append(json.loads(line))
    return vectors


VECTORS = load_vectors()


def test_vectors_present():
    assert len(VECTORS) >= 12, f"no vectors under {VECTOR_ROOT} (git submodule update --init?)"


@pytest.mark.parametrize("vector", VECTORS, ids=[v["id"] for v in VECTORS])
def test_vector_decodes(vector):
    data = bytes.fromhex(vector["hex"].replace(" ", ""))
    pkg = HuaweiSppPackage.from_bytes(data, validate_checksum=True)
    assert pkg.command_id.hex().upper() == vector["expect"]["cmd"].replace("/", ""), vector["id"]
    for tlv_type, value in vector["expect"]["tlv"].items():
        assert pkg.parameters[int(tlv_type)].hex(" ").upper() == value, f'{vector["id"]} TLV {tlv_type}'
