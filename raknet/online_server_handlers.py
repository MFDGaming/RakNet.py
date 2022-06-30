"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.connection import Connection
from raknet.misc.frame import Frame
from raknet.misc.internet_address import InternetAddress
from raknet.packet.connected_ping import ConnectedPing
from raknet.packet.connected_pong import ConnectedPong
from raknet.packet.connection_request import ConnectionRequest
from raknet.packet.connection_request_accepted import ConnectionRequestAccepted
from raknet.sc import Sc


class OnlineServerHandlers:
    def __init__(self, sc: Sc):
        self.sc: Sc = sc

    def handle_connection_request(self, frame: Frame, connection: Connection) -> None:
        connection_request: ConnectionRequest = ConnectionRequest()
        connection_request.deserialize(frame.body)
        connection_request_accepted: ConnectionRequestAccepted = ConnectionRequestAccepted()
        connection_request_accepted.client_address = connection.address
        connection_request_accepted.system_addresses = [InternetAddress()] * self.sc.system_addresses_count
        connection_request_accepted.client_timestamp = connection_request.client_timestamp
        connection_request_accepted.server_timestamp = self.sc.timestamp
        frame_to_send: Frame = Frame()
        frame_to_send.body = connection_request_accepted.serialize()
        connection.append_frame(frame_to_send, True)

    def handle_connected_ping(self, frame: Frame, connection: Connection) -> None:
        connected_ping: ConnectedPing = ConnectedPing()
        connected_ping.deserialize(frame.body)
        connected_pong: ConnectedPong = ConnectedPong()
        connected_pong.ping_timestamp = connected_ping.ping_timestamp
        connected_pong.pong_timestamp = self.sc.timestamp
        frame_to_send: Frame = Frame()
        frame_to_send.body = connected_pong.serialize()
        connection.append_frame(frame_to_send, True)