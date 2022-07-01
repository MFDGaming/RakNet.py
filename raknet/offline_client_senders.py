"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.packet.open_connection_request_one import OpenConnectionRequestOne
from raknet.packet.open_connection_request_two import OpenConnectionRequestTwo
from raknet.packet.unconnected_ping import UnconnectedPing
from raknet.sc import Sc


class OfflineClientSenders:
    def __init__(self, sc: Sc):
        self.sc: Sc = sc

    def send_unconnected_ping(self) -> None:
        unconnected_ping: UnconnectedPing = UnconnectedPing()
        unconnected_ping.client_timestamp = self.sc.timestamp
        unconnected_ping.has_client_guid = self.sc.unconnected_ping_has_client_guid
        unconnected_ping.client_guid = self.sc.guid
        self.sc.dgram.send(unconnected_ping.serialize(self.sc.has_open_connections), (self.sc.connection.address.name, self.sc.connection.address.port))

    def send_open_connection_request_one(self) -> None:
        open_connection_request_one: OpenConnectionRequestOne = OpenConnectionRequestOne()
        open_connection_request_one.protocol_version = self.sc.protocol_version
        open_connection_request_one.mtu_size = self.sc.connection.mtu_size
        self.sc.dgram.send(open_connection_request_one.serialize(), (self.sc.connection.address.name, self.sc.connection.address.port))

    def send_open_connection_request_two(self) -> None:
        open_connection_request_two: OpenConnectionRequestTwo = OpenConnectionRequestTwo()
        open_connection_request_two.server_address = self.sc.connection.address
        open_connection_request_two.mtu_size = self.sc.connection.mtu_size
        open_connection_request_two.client_guid = self.sc.guid
        self.sc.dgram.send(open_connection_request_two.serialize(), (self.sc.connection.address.name, self.sc.connection.address.port))