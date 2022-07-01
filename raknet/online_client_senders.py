"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.misc.frame import Frame
from raknet.packet.connection_request import ConnectionRequest
from raknet.sc import Sc


class OnlineClientSenders:
    def __init__(self, sc: Sc):
        self.sc: Sc = sc

    def send_connection_request(self) -> None:
        connection_request: ConnectionRequest = ConnectionRequest()
        connection_request.client_guid = self.sc.guid
        connection_request.client_timestamp = self.sc.timestamp
        frame_to_send: Frame = Frame()
        frame_to_send.body = connection_request.serialize()
        self.sc.connection.append_frame(frame_to_send, True)