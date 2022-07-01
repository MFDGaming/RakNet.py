"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.connection import Connection
from raknet.misc.frame import Frame
from raknet.misc.internet_address import InternetAddress
from raknet.offline_client_handlers import OfflineClientHandlers
from raknet.offline_client_senders import OfflineClientSenders
from raknet.online_client_handlers import OnlineClientHandlers
from raknet.online_client_senders import OnlineClientSenders
from raknet.sc import Sc
from threading import Thread
from time import sleep, time


class Client(Sc):
    def __init__(
        self,
        address: InternetAddress,
        protocol_version: int,
        default_mtu_size: int = 1500
    ):
        super().__init__(
            address,
            protocol_version,
            False
        )
        self.default_mtu_size: int = default_mtu_size
        self.state: int = 0
        self.has_open_connections: bool = False
        self.unconnected_ping_has_client_guid: bool = True
        self.connection: Connection = Connection(address, self.default_mtu_size, self)
        self.offline_client_handlers: OfflineClientHandlers = OfflineClientHandlers(self)
        self.offline_client_senders: OfflineClientSenders = OfflineClientSenders(self)
        self.online_client_handlers: OnlineClientHandlers = OnlineClientHandlers(self)
        self.online_client_senders: OnlineClientSenders = OnlineClientSenders(self)
        self.worker_thread: Thread = Thread(target=self.handle_task)
        self.worker_thread.start()

    def disconnect(self) -> None:
        self.disconnected_handler(self.connection)
        if self.state == 3:
            self.connection.disconnect()
        self.state = 0

    def connect(self) -> None:
        self.state = 1

    def set_connecting(self) -> None:
        self.state = 2

    def set_connected(self) -> None:
        self.state = 3

    def handle_frame(self, frame: Frame, connection: Connection) -> None:
        if not self.connection.has_connected:
            if frame.body[0] == 0x10:
                self.online_client_handlers.handle_connection_request_accepted(frame)
                self.connected_handler(self.connection)
        else:
            if frame.body[0] == 0x15:
                self.disconnect()
            elif frame.body[0] == 0x03:
                pass # just do nothing about it
            elif frame.body[0] == 0x00:
                self.connection.handle_connected_ping(frame)
            else:
                self.frame_handler(frame, self.connection)

    def handle_task(self) -> None:
        connection_request_sent: bool = False
        while self.is_running:
            start: float = time()
            for i in range(5000):
                recv = self.dgram.receive()
                try:
                    if self.state == 0:
                        if recv and recv[0][0] == 0x1c:
                            self.offline_client_handlers.handle_unconnected_pong(recv[0])
                        else:
                            self.offline_client_senders.send_unconnected_ping()
                    elif self.state == 1:
                        if recv and recv[0][0] == 0x06:
                            self.offline_client_handlers.handle_open_connection_reply_one(recv[0])
                        else:
                            self.offline_client_senders.send_open_connection_request_one()
                            if self.connection.mtu_size == 0:
                                self.connection.mtu_size = self.default_mtu_size
                            else:
                                self.connection.mtu_size -= 1
                    elif self.state == 2:
                        if recv and recv[0][0] == 0x08:
                            self.offline_client_handlers.handle_open_connection_reply_two(recv[0])
                        else:
                            self.offline_client_senders.send_open_connection_request_two()
                    elif self.state == 3:
                        if recv:
                            self.connection.handle(recv[0])
                        if not connection_request_sent and not self.connection.has_connected:
                            self.online_client_senders.send_connection_request()
                            connection_request_sent = True
                except Exception as e:
                    print(e)
            diff: float = time() - start
            if diff < 0.05:
                sleep(0.05 - diff)
            if self.state == 3:
                if (time() - self.connection.last_update_time) >= 10:
                    self.disconnect()
                else:
                    self.connection.tick()
