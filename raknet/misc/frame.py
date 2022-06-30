"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack
from raknet.misc.reliability import Reliability


class Frame:
    def __init__(self):
        self.reliability: int = 0
        self.is_fragmented: bool = False
        self.reliable_index: int = 0
        self.sequenced_index: int = 0
        self.ordered_index: int = 0
        self.order_channel: int = 0
        self.compound_size: int = 0
        self.compound_id: int = 0
        self.compound_entry_index: int = 0
        self.body: bytes = b""

    @property
    def is_reliable(self) -> bool:
        if (
            self.reliability == Reliability.RELIABLE or
            self.reliability == Reliability.RELIABLE_ORDERED or
            self.reliability == Reliability.RELIABLE_SEQUENCED or
            self.reliability == Reliability.RELIABLE_WITH_ACK_RECEIPT or
            self.reliability == Reliability.RELIABLE_ORDERED_WITH_ACK_RECEIPT
        ):
            return True
        return False

    @property
    def is_sequenced(self) -> bool:
        if (
            self.reliability == Reliability.UNRELIABLE_SEQUENCED or
            self.reliability == Reliability.RELIABLE_SEQUENCED
        ):
            return True
        return False

    @property
    def is_ordered(self) -> bool:
        if (
            self.reliability == Reliability.UNRELIABLE_SEQUENCED or
            self.reliability == Reliability.RELIABLE_ORDERED or
            self.reliability == Reliability.RELIABLE_SEQUENCED or
            self.reliability == Reliability.RELIABLE_ORDERED_WITH_ACK_RECEIPT
        ):
            return True
        return False

    @property
    def size(self) -> int:
        return (
            3 +
            len(self.body) +
            (3 if self.is_reliable else 0) +
            (3 if self.is_sequenced else 0) +
            (4 if self.is_ordered else 0) +
            (10 if self.is_fragmented else 0)
        )

    def deserialize(self, data: bytes) -> int:
        flags: int = unpack("B", data[0:1])[0]
        self.reliability = (flags & 0xe0) >> 5
        self.is_fragmented = (flags & 0x10) > 0
        body_size: int = unpack(">H", data[1:3])[0] >> 3
        offset: int = 3
        if self.is_reliable:
            self.reliable_index = int.from_bytes(
                data[offset:offset+3],
                "little"
            )
            offset += 3
        if self.is_sequenced:
            self.sequenced_index = int.from_bytes(
                data[offset:offset+3],
                "little"
            )
            offset += 3
        if self.is_ordered:
            self.ordered_index = int.from_bytes(
                data[offset:offset+3],
                "little"
            )
            offset += 3
            self.order_channel = unpack(
                "B",
                data[offset:offset+1]
            )[0]
            offset += 1
        if self.is_fragmented:
            self.compound_size = unpack(
                ">L",
                data[offset:offset+4]
            )[0]
            offset += 4
            self.compound_id = unpack(
                ">H",
                data[offset:offset+2]
            )[0]
            offset += 2
            self.compound_entry_index = unpack(
                ">L",
                data[offset:offset+4]
            )[0]
            offset += 4
        self.body = data[offset:offset+body_size]
        offset += body_size
        return offset

    def serialize(self) -> bytes:
        return (
            pack(
                "B",
                (
                    (self.reliability << 5) |
                    (0x10 if self.is_fragmented else 0x00)
                )
            ) +
            pack(">H", len(self.body) << 3) +
            (
                int.to_bytes(
                    self.reliable_index,
                    3,
                    "little"
                ) if self.is_reliable else b""
            ) +
            (
                int.to_bytes(
                    self.sequenced_index,
                    3,
                    "little"
                ) if self.is_sequenced else b""
            ) +
            (
                int.to_bytes(
                    self.ordered_index,
                    3,
                    "little"
                ) if self.is_ordered else b""
      	    ) +
            (
                (
                    pack(">L", self.compound_size) +
                    pack(">H", self.compound_id) +
                    pack(">L", self.compound_entry_index)
                ) if self.is_fragmented else b""
            ) +
            self.body
        )
