"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.misc.frame import Frame
from raknet.misc.internet_address import InternetAddress
from raknet.packet.new_incoming_connection import NewIncomingConnection
from raknet.packet.connection_request_accepted import ConnectionRequestAccepted
from raknet.sc import Sc


class OnlineClientHandlers:
    def __init__(self, sc: Sc):
        self.sc: Sc = sc

    def handle_connection_request_accepted(self, frame: Frame) -> None:
        connection_request_accepted: ConnectionRequestAccepted = ConnectionRequestAccepted()
        connection_request_accepted.deserialize(frame.body)
        new_incoming_connection: NewIncomingConnection = NewIncomingConnection()
        new_incoming_connection.server_address = self.sc.connection.address
        new_incoming_connection.system_addresses = [InternetAddress()] * self.sc.system_addresses_count
        new_incoming_connection.server_timestamp = connection_request_accepted.server_timestamp
        new_incoming_connection.client_timestamp = self.sc.timestamp
        frame_to_send: Frame = Frame()
        frame_to_send.body = new_incoming_connection.serialize()
        self.sc.connection.append_frame(frame_to_send, True)
        self.sc.connection.has_connected = True