"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from struct import unpack, pack


class Acknowledge:
    def __init__(self):
        self.sequence_numbers: list = []

    def deserialize(self, data: bytes) -> None:
        record_count: int = unpack(">H", data[1:3])[0]
        offset: int = 3
        for _ in range(record_count):
            is_single: bool = unpack("?",
                data[offset:offset+1]
            )[0]
            offset += 1
            if is_single:
                self.sequence_numbers.append(
                    int.from_bytes(
                        data[offset:offset+3],
                        "little"
                    )
                )
                offset += 3
            else:
                current: int = int.from_bytes(
                    data[offset:offset+3],
                    "little"
                )
                offset += 3
                end: int = int.from_bytes(
                    data[offset:offset+3],
                    "little"
                )
                offset += 3
                while (current <= end):
                    self.sequence_numbers.append(current)
                    current += 1

    def serialize_base(self, packet_id: bytes) -> bytes:
        self.sequence_numbers.sort()
        data: bytes = b""
        record_count: int = 0
        if self.sequence_numbers:
            start: int = self.sequence_numbers[0]
            end: int = self.sequence_numbers[0]
            for i in range(1, len(self.sequence_numbers)):
                current: int = self.sequence_numbers[i]
                diff: int = current - end
                if diff == 1:
                    end = current
                elif diff > 1:
                    if start == end:
                        data += (
                            b"\x01" +
                            int.to_bytes(start, 3, "little")
                        )
                    else:
                        data += (
                            b"\x00" +
                            int.to_bytes(start, 3, "little") +
                            int.to_bytes(end, 3, "little")
                        )
                    start = end = current
                    record_count += 1
            if start == end:
                data += (
                    b"\x01" +
                    int.to_bytes(start, 3, "little")
                )
            else:
                data += (
                    b"\x00" +
                    int.to_bytes(start, 3, "little") +
                    int.to_bytes(end, 3, "little")
                )
            record_count += 1
        return packet_id + pack(">H", record_count) + data
