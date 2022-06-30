"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.internet_address import InternetAddress


class ConnectionRequestAccepted:
    def __init__(self):
        self.client_address: InternetAddress = None
        self.system_index: int = 0
        self.system_addresses: list = []
        self.client_timestamp: int = 0
        self.server_timestamp: int = 0

    def deserialize(self, data: bytes) -> None:
        self.client_address = InternetAddress()
        self.client_address.deserialize(data[1:])
        system_address_data: bytes = None
        if self.client_address.version == 4:
            self.system_index = unpack(">H", data[8:10])[0]
            system_address_data = data[10:-16]
        elif self.client_address.version == 6:
            self.system_index = unpack(">H", data[30:32])[0]
            system_address_data = data[32:-16]
        self.client_timestamp = unpack(">Q", data[-16:-8])[0]
        self.server_timestamp = unpack(">Q", data[-8:])[0]
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
            b"\x10" +
            self.client_address.serialize() +
            pack(">H", self.system_index) +
            b"".join(
                x.serialize() for x in self.system_addresses
            ) +
            pack(">Q", self.client_timestamp) +
            pack(">Q", self.server_timestamp)
        )
