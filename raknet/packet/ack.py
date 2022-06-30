"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.packet.acknowledge import Acknowledge


class Ack(Acknowledge):
    def serialize(self) -> bytes:
        return self.serialize_base(b"\xc0")