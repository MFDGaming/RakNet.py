"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.misc.internet_address import InternetAddress
from raknet.packet.incompatible_protocol_version import IncompatibleProtocolVersion
from raknet.packet.open_connection_reply_one import OpenConnectionReplyOne
from raknet.packet.open_connection_reply_two import OpenConnectionReplyTwo
from raknet.packet.open_connection_request_one import OpenConnectionRequestOne
from raknet.packet.open_connection_request_two import OpenConnectionRequestTwo
from raknet.packet.unconnected_ping import UnconnectedPing
from raknet.packet.unconnected_pong import UnconnectedPong
from raknet.sc import Sc


class OfflineServerHandlers():
    def __init__(self, sc: Sc):
        self.sc: Sc = sc

    def handle_unconnected_ping(self, data: bytes, address: InternetAddress) -> None:
        unconnected_ping: UnconnectedPing = UnconnectedPing()
        unconnected_ping.deserialize(data)
        unconnected_pong: UnconnectedPong = UnconnectedPong()
        unconnected_pong.client_timestamp = unconnected_ping.client_timestamp
        unconnected_pong.server_guid = self.sc.guid
        unconnected_pong.data = self.sc.message.encode()
        self.sc.dgram.send(unconnected_pong.serialize(), (address.name, address.port))

    def handle_open_connection_request_one(self, data: bytes, address: InternetAddress) -> None:
        open_connection_request_one: OpenConnectionRequestOne = OpenConnectionRequestOne()
        open_connection_request_one.deserialize(data)
        if open_connection_request_one.protocol_version == self.sc.protocol_version:
            open_connection_reply_one: OpenConnectionReplyOne = OpenConnectionReplyOne()
            open_connection_reply_one.server_guid = self.sc.guid
            open_connection_reply_one.use_security = False
            open_connection_reply_one.mtu_size = open_connection_request_one.mtu_size
            self.sc.dgram.send(open_connection_reply_one.serialize(), (address.name, address.port))
        else:
            incompatible_protocol_version: IncompatibleProtocolVersion = IncompatibleProtocolVersion()
            incompatible_protocol_version.protocol_version = open_connection_request_one.protocol_version
            incompatible_protocol_version.server_guid = self.sc.guid
            self.sc.dgram.send(incompatible_protocol_version.serialize(), (address.name, address.port))
        
    def handle_open_connection_request_two(self, data: bytes, address: InternetAddress) -> None:
        open_connection_request_two: OpenConnectionRequestTwo = OpenConnectionRequestTwo()
        open_connection_request_two.deserialize(data)
        open_connection_reply_two: OpenConnectionReplyTwo = OpenConnectionReplyTwo()
        open_connection_reply_two.server_guid = self.sc.guid
        open_connection_reply_two.client_address = address
        open_connection_reply_two.mtu_size = open_connection_request_two.mtu_size
        open_connection_reply_two.use_encryption = False
        self.sc.dgram.send(open_connection_reply_two.serialize(), (address.name, address.port))
        self.sc.add_connection(address, open_connection_reply_two.mtu_size)