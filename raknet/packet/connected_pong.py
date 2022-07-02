"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack


class ConnectedPong:
    def __init__(self):
        self.ping_timestamp: int = 0
        self.pong_timestamp: int = 0

    def deserialize(self, data: bytes) -> None:
        self.ping_timestamp = unpack(">Q", data[1:9])[0]
        self.pong_timestamp = unpack(">Q", data[9:17])[0]

    def serialize(self) -> bytes:
        return (
            b"\x03" +
            pack(">Q", self.ping_timestamp) +
            pack(">Q", self.pong_timestamp)
        )
