"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from copy import copy
from raknet.connection import Connection
from raknet.misc.frame import Frame
from raknet.misc.internet_address import InternetAddress
from raknet.offline_server_handlers import OfflineServerHandlers
from raknet.online_server_handlers import OnlineServerHandlers
from raknet.sc import Sc
from threading import Thread
from time import sleep, time


class Server(Sc):
    def __init__(
        self,
        address: InternetAddress,
        protocol_version: int
    ):
        super().__init__(address, protocol_version, True)
        self.connections: dict = {}
        self.offline_handlers: OfflineServerHandlers = OfflineServerHandlers(self)
        self.online_server_handlers: OnlineServerHandlers = OnlineServerHandlers(self)
        self.worker_thread: Thread = Thread(target=self.handle_task)
        self.worker_thread.start()

    def handle_frame(self, frame: Frame, connection: Connection) -> None:
        if not connection.has_connected:
            if frame.body[0] == 0x09:
                self.online_server_handlers.handle_connection_request(frame, connection)
            elif frame.body[0] == 0x13:
                connection.has_connected = True
                self.connected_handler(connection)
        else:
            if frame.body[0] == 0x00:
                self.online_server_handlers.handle_connected_ping(frame, connection)
            elif frame.body[0] == 0x15:
                self.remove_connection(connection.address)
            else:
                self.frame_handler(frame, connection)

    def handle_task(self) -> None:
        while self.is_running:
            recv: tuple = self.dgram.receive()
            try:
                if recv:
                    address: InternetAddress = InternetAddress(
                        recv[1][0],
                        recv[1][1],
                        self.address.version
                    )
                    if recv[0][0] == 0x01 or recv[0][0] == 0x02:
                        self.offline_handlers.handle_unconnected_ping(recv[0], address)
                    elif recv[0][0] == 0x05:
                        self.offline_handlers.handle_open_connection_request_one(recv[0], address)
                    elif recv[0][0] == 0x07:
                        self.offline_handlers.handle_open_connection_request_two(recv[0], address)
                    else:
                        connection: Connection = self.get_connection(address)
                        if connection is not None:
                            connection.handle(recv[0])
            except Exception as e:
                print(e)
            for connection in list(self.connections.values()):
                if (time() - connection.last_update_time) >= 10:
                    self.remove_connection(connection.address)
                else:
                    connection.tick()
            sleep(0.05)

    def add_connection(
        self,
        address: InternetAddress,
        mtu_size: int
    ) -> None:
        self.connections[address.token] = Connection(
            address,
            mtu_size,
            self
        )

    def remove_connection(
        self,
        address: InternetAddress
    ) -> None:
        if address.token in self.connections:
            self.disconnected_handler(self.connections[address.token])
            self.connections[address.token].disconnect()
            del self.connections[address.token]

    def get_connection(
        self,
        address: InternetAddress
    ) -> None:
        if address.token in self.connections:
            return self.connections[address.token]

    def has_connection(
        self,
        address: InternetAddress
    ) -> None:
        return (address.token in self.connections)
