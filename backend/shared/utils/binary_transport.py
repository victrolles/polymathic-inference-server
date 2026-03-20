import pickle
import zlib
from typing import Any


def to_binary_payload(payload: Any) -> bytes:
    """Serialize a python payload into compressed binary bytes."""
    serialized = pickle.dumps(payload, protocol=pickle.HIGHEST_PROTOCOL)
    return zlib.compress(serialized)


def from_binary_payload(payload: bytes) -> Any:
    """Deserialize compressed binary bytes into a python payload."""
    serialized = zlib.decompress(payload)
    return pickle.loads(serialized)
