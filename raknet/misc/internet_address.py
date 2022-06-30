"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import pack, unpack
from socket import inet_ntop, inet_pton, AF_INET6


class InternetAddress:
    def __init__(self, name: str = "0.0.0.0", port: int = 0, version: int = 4):
        self.name = name
        self.port = port
        self.version = version

    @property
    def token(self) -> str:
        return self.name + ":" + str(self.port)

    def deserialize(self, data: bytes) -> None:
        self.version = unpack("B", data[0:1])[0]
        if self.version == 4:
            # 7
            self.name = ".".join([
                str(~unpack("B", data[1:2])[0] & 0xff),
                str(~unpack("B", data[2:3])[0] & 0xff),
                str(~unpack("B", data[3:4])[0] & 0xff),
                str(~unpack("B", data[4:5])[0] & 0xff)
            ])
            self.port = unpack(">H", data[5:7])[0]
        elif self.version == 6:
            # 29
            self.port = unpack(">H", data[3:5])[0]
            self.name = inet_ntop(
                AF_INET6,
                data[9:25]
            )

    def serialize(self) -> bytes:
        if self.version == 4:
            parts: list = self.name.split(".")
            return (
                pack("B", self.version) +
                pack("B", ~int(parts[0]) & 0xff) +
                pack("B", ~int(parts[1]) & 0xff) +
                pack("B", ~int(parts[2]) & 0xff) +
                pack("B", ~int(parts[3]) & 0xff) +
                pack(">H", self.port)
            )
        elif self.version == 6:
            return (
                pack("B", self.version) +
                pack("<H", AF_INET6) +
                pack(">H", self.port) +
                b"\x00\x00\x00\x00" +
                inet_pton(
                    AF_INET6,
                    self.name
                ) +
                b"\x00\x00\x00\x00"
            )
