"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.magic import Magic
from raknet.misc.internet_address import InternetAddress


class OpenConnectionRequestTwo:
    def __init__(self):
        self.server_address: InternetAddress = None
        self.mtu_size: int = 0
        self.client_guid: int = 0

    def deserialize(self, data: bytes) -> None:
        Magic.validate(data[1:17])
        self.server_address = InternetAddress()
        self.server_address.deserialize(
            data[17:]
        )
        if self.server_address.version == 4:
            self.mtu_size = unpack(">H",
                data[24:26]
            )[0]
            self.client_guid = unpack(">Q",
       	        data[26:34]
            )[0]
        elif self.server_address.version == 6:
            self.mtu_size = unpack(">H",
                data[46:48]
            )[0]
            self.client_guid = unpack(">Q",
                data[48:56]
            )[0]

    def serialize(self) -> bytes:
        return (
            b"\x07" +
            Magic.id +
            self.server_address.serialize() +
            pack(">H", self.mtu_size) +
            pack(">Q", self.client_guid)
        )

