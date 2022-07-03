"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.misc.frame import Frame


class FrameSet:
    def __init__(self):
        self.sequence_number: int = 0
        self.frames: list = []
        self.send_time: float = 0.0

    def deserialize(self, data: bytes) -> None:
        self.sequence_number = int.from_bytes(
            data[1:4],
            "little"
        )
        offset: int = 4
        while offset < len(data[4:]):
            frame: Frame = Frame()
            offset += frame.deserialize(data[offset:])
            self.frames.append(frame)
            
    def serialize(self) -> bytes:
        return (
            b"\x80" +
            int.to_bytes(
                self.sequence_number & 0xffffff,
                3,
                "little"
            ) +
            b"".join(
                x.serialize() for x in self.frames
            )
        )
