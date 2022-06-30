"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.magic import Magic


class OpenConnectionRequestOne:
    def __init__(self):
        self.protocol_version: int = 0
        self.mtu_size: int = 0

    def deserialize(self, data: bytes) -> None:
        Magic.validate(data[1:17])
        self.protocol_version = unpack("B", data[17:18])[0]
        self.mtu_size = len(data) + 28

    def serialize(self) -> bytes:
        return (
            b"\x05" +
            Magic.id +
            pack("B", self.protocol_version) +
            b"\x00" * (self.mtu_size - 46)
        )
