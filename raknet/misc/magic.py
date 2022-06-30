"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.misc.errors import InvalidMagic


class Magic:
    id = bytes([
        0x00, 0xff, 0xff, 0x00,
        0xfe, 0xfe, 0xfe, 0xfe,
        0xfd, 0xfd, 0xfd, 0xfd,
        0x12, 0x34, 0x56, 0x78
    ])

    @staticmethod
    def validate(data: bytes) -> bool:
        if data != Magic.id:
            raise InvalidMagic("Invalid magic id")
