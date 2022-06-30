"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.internet_address import InternetAddress


class NewIncomingConnection:
    def __init__(self):
        self.server_address: InternetAddress = None
        self.system_addresses: list = []
        self.server_timestamp: int = 0
        self.client_timestamp: int = 0

    def deserialize(self, data: bytes) -> None:
        self.server_address = InternetAddress()
        self.server_address.deserialize(data[1:])
        system_address_data: bytes = None
        if self.server_address.version == 4:
            system_address_data = data[8:-16]
        elif self.server_address.version == 6:
            system_address_data = data[30:-16]
        self.server_timestamp = unpack(">Q", data[-16:-8])[0]
        self.client_timestamp = unpack(">Q", data[-8:])[0]
        self.system_addresses = []
        offset: int = 0
        while offset < len(system_address_data):
            address: InternetAddress = InternetAddress()
            address.deserialize(system_address_data[offset:])
            self.system_addresses.append(address)
            if address.version == 4:
                offset += 7
            elif address.version == 6:
                offset += 29

    def serialize(self) -> bytes:
        return (
            b"\x13" +
            self.server_address.serialize() +
            b"".join(
                x.serialize() for x in self.system_addresses
            ) +
            pack(">Q", self.server_timestamp) +
            pack(">Q", self.client_timestamp)
        )
