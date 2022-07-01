"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.magic import Magic


class UnconnectedPing:
    def __init__(self):
        self.client_timestamp: int = 0
        self.has_client_guid: bool = True
        self.client_guid: int = 0

    def deserialize(self, data: bytes) -> None:
        self.client_timestamp = unpack(">Q", data[1:9])[0]
        Magic.validate(data[9:25])
        if len(data) > 25:
            self.has_client_guid = True
            self.client_guid = unpack(">Q", data[25:33])[0]
        else:
            self.has_client_guid = False

    def serialize(self, has_open_connections: bool = False) -> bytes:
        return (
            (b"\x01" if not has_open_connections else b"\x02") +
            pack(">Q", self.client_timestamp) +
            Magic.id +
            (pack(">Q", self.client_guid) if self.has_client_guid else b"")
        )
