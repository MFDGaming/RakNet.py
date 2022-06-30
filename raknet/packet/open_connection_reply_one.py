"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.magic import Magic


class OpenConnectionReplyOne:
    def __init__(self):
        self.server_guid: int = 0
        self.use_security: bool = False
        self.mtu_size: int = 0

    def deserialize(self, data: bytes) -> None:
        Magic.validate(data[1:17])
        self.server_guid = unpack(">Q", data[17:25])[0]
        self.use_security = unpack("?", data[25:26])[0]
        self.mtu_size = unpack(">H", data[26:28])[0]

    def serialize(self) -> bytes:
        return (
            b"\x06" +
            Magic.id +
            pack(">Q", self.server_guid) +
            pack("?", self.use_security) +
            pack(">H", self.mtu_size)
        )
