"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.packet.open_connection_reply_one import OpenConnectionReplyOne
from raknet.packet.open_connection_reply_two import OpenConnectionReplyTwo
from raknet.packet.unconnected_pong import UnconnectedPong
from raknet.sc import Sc


class OfflineClientHandlers:
    def __init__(self, sc: Sc):
        self.sc: Sc = sc

    def handle_unconnected_pong(self, data: bytes) -> None:
        unconnected_pong: UnconnectedPong = UnconnectedPong()
        unconnected_pong.deserialize(data)
        self.sc.message = unconnected_pong.data.decode()

    def handle_open_connection_reply_one(self, data: bytes) -> None:
        open_connection_reply_one: OpenConnectionReplyOne = OpenConnectionReplyOne()
        open_connection_reply_one.deserialize(data)
        self.sc.connection.mtu_size = min(open_connection_reply_one.mtu_size, self.sc.connection.mtu_size)
        self.sc.set_connecting()

    def handle_open_connection_reply_two(self, data: bytes) -> None:
        open_connection_reply_two: OpenConnectionReplyTwo = OpenConnectionReplyTwo()
        open_connection_reply_two.deserialize(data)
        self.sc.connection.mtu_size = min(open_connection_reply_two.mtu_size, self.sc.connection.mtu_size)
        self.sc.set_connected()