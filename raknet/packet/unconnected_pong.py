"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.magic import Magic


class UnconnectedPong:
    def __init__(self):
        self.client_timestamp: int = 0
        self.server_guid: int = 0
        self.data: bytes = b""

    def deserialize(self, data: bytes) -> None:
        self.client_timestamp = unpack(">Q", data[1:9])[0]
        self.server_guid = unpack(">Q", data[9:17])[0]
        Magic.validate(data[17:33])
        length: int = unpack(">H", data[33:35])[0]
        self.data = data[35:35+length]

    def serialize(self) -> bytes:
        return (
            b"\x1c" +
            pack(">Q", self.client_timestamp) +
            pack(">Q", self.server_guid) +
            Magic.id +
            pack(">H", len(self.data)) +
            self.data
        )
