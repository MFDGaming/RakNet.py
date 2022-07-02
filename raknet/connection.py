"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from math import ceil
from raknet.misc.frame import Frame
from raknet.misc.internet_address import InternetAddress
from raknet.misc.reliability import Reliability
from raknet.packet.ack import Ack
from raknet.packet.connected_ping import ConnectedPing
from raknet.packet.connected_pong import ConnectedPong
from raknet.packet.frame_set import FrameSet
from raknet.packet.nack import Nack
from raknet.sc import Sc
from time import time


class Connection:
    def __init__(self, address: InternetAddress, mtu_size: int, sc: Sc):
        self.address: InternetAddress = address
        self.mtu_size = mtu_size
        self.sc: Sc = sc
        self.has_connected: bool = False
        self.last_update_time: float = time()
        self.ack_queue: list = []
        self.nack_queue: list = []
        self.sender_sequence_number: int = 0
        self.receiver_sequence_number: int = 0
        self.sender_reliable_index: int = 0
        self.receiver_reliable_index: int = 0
        self.sender_sequence_channels: list = [0] * 32
        self.sender_order_channels: list = [0] * 32
        self.sender_compound_id: int = 0
        self.queue: list = []
        self.frame_holder: dict = {}
        self.recovery_queue: dict = {}
        self.wait_for_pong: bool = False
        self.ms: int = 0

    def send_ack_queue(self) -> None:
        if self.ack_queue:
            ack: Ack = Ack()
            ack.sequence_numbers = self.ack_queue
            self.sc.dgram.send(ack.serialize(), (self.address.name, self.address.port))
            self.ack_queue = []

    def send_nack_queue(self) -> None:
        if self.nack_queue:
            ack: Nack = Ack()
            ack.sequence_numbers = self.ack_queue
            self.sc.dgram.send(ack.serialize(), (self.address.name, self.address.port))
            self.ack_queue = []

    def send_frames(self, frames: list) -> None:
        frame_set: FrameSet = FrameSet()
        frame_set.sequence_number = self.sender_sequence_number
        frame_set.frames = frames
        self.sender_sequence_number += 1
        frame_set.send_time = time()
        self.recovery_queue[frame_set.sequence_number] = frame_set
        self.sc.dgram.send(frame_set.serialize(), (self.address.name, self.address.port))

    def send_queue(self) -> None:
        if self.queue:
            self.send_frames(self.queue)
            self.queue = []

    def append_frame(self, frame: Frame, is_immediate: bool) -> None:
        if is_immediate:
            self.send_frames([frame])
        else:
            size = 4 + frame.size
            for entry in self.queue:
                size += entry.size
            if size > (self.mtu_size - 36):
                self.send_queue()
            self.queue.append(frame)

    def add_to_queue(self, frame: Frame) -> None:
        if frame.is_sequenced:
            frame.ordered_index = self.sender_order_channels[frame.order_channel]
            frame.sequenced_index = self.sender_sequence_channels[frame.order_channel]
            self.sender_sequence_channels[frame.order_channel] += 1
        elif frame.is_ordered:
            frame.ordered_index = self.sender_order_channels[frame.order_channel]
            self.sender_order_channels[frame.order_channel] += 1
        max_size = self.mtu_size - 60
        if len(frame.body) > max_size:
            compound_size: int = ceil(len(frame.body) / max_size)
            self.sender_compound_id &= 0xffff
            offset: int = 0
            for i in range(compound_size):
                compound_entry: Frame = Frame()
                compound_entry.is_fragmented = True
                compound_entry.reliability = frame.reliability
                compound_entry.compound_size = compound_size
                compound_entry.compound_id = self.sender_compound_id
                compound_entry.compound_entry_index = i
                compound_entry.body = frame.body[offset:offset + max_size]
                offset += max_size
                if frame.is_reliable:
                    compound_entry.reliable_index = self.sender_reliable_index
                    self.sender_reliable_index += 1
                if frame.is_ordered:
                    compound_entry.ordered_index = frame.ordered_index
                    compound_entry.order_channel = frame.order_channel
                if frame.is_sequenced:
                    compound_entry.sequenced_index = frame.sequenced_index
                self.append_frame(compound_entry, True)
            self.sender_compound_id += 1
        else:
            if frame.is_reliable:
                frame.reliable_index = self.sender_reliable_index
                self.sender_reliable_index += 1
            self.append_frame(frame, False)

    def disconnect(self) -> None:
        frame: Frame = Frame()
        frame.is_fragmented = False
        frame.reliability = Reliability.UNRELIABLE
        frame.body = b"\x13"
        self.append_frame(frame, True)

    def handle_ack(self, data: bytes) -> None:
        ack: Ack = Ack()
        ack.deserialize(data)
        for sequence_number in ack.sequence_numbers:
            if sequence_number in self.recovery_queue:
                del self.recovery_queue[sequence_number]
                break

    def handle_nack(self, data: bytes) -> None:
        nack: Nack = Nack()
        nack.deserialize(data)
        for sequence_number in nack.sequence_numbers:
            if sequence_number in self.recovery_queue:
                self.send_frames(self.recovery_queue[sequence_number].frames)
                del self.recovery_queue[sequence_number]
                break

    def handle_fragmented_frame(self, frame: Frame) -> None:
        if frame.compound_id not in self.frame_holder:
            self.frame_holder[frame.compound_id] = {frame.compound_entry_index: frame}
        else:
            self.frame_holder[frame.compound_id][frame.compound_entry_index] = frame
        if len(self.frame_holder[frame.compound_id]) == frame.compound_size:
            compound: Frame = Frame()
            compound.reliability = frame.reliability
            compound.sequenced_index = frame.sequenced_index
            compound.ordered_index = frame.ordered_index
            compound.order_channel = frame.order_channel
            for i in range(frame.compound_size):
                compound.body += self.frame_holder[frame.compound_id][i].body
            del self.frame_holder[frame.compound_id]
            self.handle_frame(compound)

    def handle_frame(self, frame: Frame) -> None:
        if frame.is_fragmented:
            self.handle_fragmented_frame(frame)
        else:
            self.sc.handle_frame(frame, self)

    def handle_frame_set(self, data: bytes) -> None:
        frame_set: FrameSet = FrameSet()
        frame_set.deserialize(data)
        if frame_set.sequence_number in self.nack_queue:
            self.nack_queue.remove(frame_set.sequence_number)
        if frame_set.sequence_number not in self.ack_queue:
            self.ack_queue.append(frame_set.sequence_number)
        hole_size: int = frame_set.sequence_number - self.receiver_sequence_number
        if not hole_size:
            for sequence_number in range(self.receiver_sequence_number + 1, frame_set.sequence_number):
                if sequence_number not in self.nack_queue:
                    self.nack_queue.append(sequence_number)
        self.receiver_sequence_number = frame_set.sequence_number + 1
        for frame in frame_set.frames:
            self.handle_frame(frame)

    def handle(self, data: bytes) -> None:
        self.last_update_time = time()
        if data[0] == 0xc0:
            self.handle_ack(data)
        elif data[0] == 0xa0:
            self.handle_nack(data)
        elif 0x80 <= data[0] <= 0x8f:
            self.handle_frame_set(data)

    def send_connected_ping(self) -> None:
        self.wait_for_pong = True
        connected_ping: ConnectedPing = ConnectedPing()
        connected_ping.ping_timestamp = self.sc.timestamp
        frame_to_send: Frame = Frame()
        frame_to_send.body = connected_ping.serialize()
        self.append_frame(frame_to_send, True)

    def handle_connected_ping(self, frame: Frame) -> None:
        connected_ping: ConnectedPing = ConnectedPing()
        connected_ping.deserialize(frame.body)
        connected_pong: ConnectedPong = ConnectedPong()
        connected_pong.ping_timestamp = connected_ping.ping_timestamp
        connected_pong.pong_timestamp = self.sc.timestamp
        frame_to_send: Frame = Frame()
        frame_to_send.body = connected_pong.serialize()
        self.append_frame(frame_to_send, True)

    def handle_connected_pong(self, frame: Frame) -> None:
        connected_pong: ConnectedPong = ConnectedPong()
        connected_pong.deserialize(frame.body)
        self.ms = self.sc.timestamp - connected_pong.ping_timestamp
        self.wait_for_pong = False

    def tick(self) -> None:
        self.send_ack_queue()
        self.send_nack_queue()
        self.send_queue()
        for frame_set in list(self.recovery_queue.values()):
            if frame_set.send_time < (time() - 8):
                self.send_frames(frame_set.frames)
                del self.recovery_queue[frame_set.sequence_number]
        if self.has_connected:
            if not self.wait_for_pong:
                self.send_connected_ping()
