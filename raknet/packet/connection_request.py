"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack


class ConnectionRequest:
    def __init__(self):
        self.client_guid: int = 0
        self.client_timestamp: int = 0
        self.use_security: bool = False

    def deserialize(self, data: bytes) -> None:
        self.client_guid = unpack(">Q", data[1:9])[0]
        self.client_timestamp = unpack(">Q", data[9:17])[0]
        self.use_security = unpack("?", data[17:18])[0]

    def serialize(self) -> bytes:
        return (
            b"\x09" +
            pack(">Q", self.client_guid) +
            pack(">Q", self.client_timestamp) +
            pack("?", self.use_security)
        )
