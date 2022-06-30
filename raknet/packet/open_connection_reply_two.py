"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.magic import Magic
from raknet.misc.internet_address import InternetAddress


class OpenConnectionReplyTwo:
    def __init__(self):
        self.server_guid: int = 0
        self.client_address: InternetAddress = None
        self.mtu_size: int = 0
        self.use_encryption: bool = False

    def deserialize(self, data: bytes) -> None:
        Magic.validate(data[1:17])
        self.server_guid = unpack(">Q", data[17:25])[0]
        self.client_address = InternetAddress()
        self.client_address.deserialize(
            data[25:]
        )
        if self.client_address.version == 4:
            self.mtu_size = unpack(">H",
                data[32:34]
            )[0]
            self.use_encryption = unpack("?",
                data[34:35]
            )[0]
        elif self.client_address.version == 6:
            self.mtu_size = unpack(">H",
                data[54:56]
            )[0]
            self.use_encryption = unpack("?",
                data[56:57]
            )[0]

    def serialize(self) -> bytes:
        return (
            b"\x08" +
            Magic.id +
            pack(">Q", self.server_guid) +
            self.client_address.serialize() +
            pack(">H", self.mtu_size) +
            pack("?", self.use_encryption)
        )
