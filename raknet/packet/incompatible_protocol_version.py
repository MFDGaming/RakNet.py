"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.magic import Magic


class IncompatibleProtocolVersion:
    def __init__(self):
        self.protocol_version: int = 0
        self.server_guid: int = 0

    def deserialize(self, data: bytes) -> None:
        self.protocol_version = unpack("B", data[1:2])[0]
        Magic.validate(data[2:18])
        self.server_guid = unpack(">Q", data[18:26])[0]

    def serialize(self) -> bytes:
        return (
            b"\x19" +
            pack("B", self.protocol_version) +
            Magic.id +
            pack(">Q", self.server_guid)
        )

