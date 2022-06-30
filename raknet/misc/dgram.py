"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.misc.internet_address import InternetAddress
from raknet.misc.errors import (
    InvalidAddressVersion,
    InvalidPort,
    PortInUse,
    FailedToBindPort
)
from socket import (
    socket as Socket,
    AF_INET,
    AF_INET6,
    SOCK_DGRAM,
    IPPROTO_UDP,
    IPPROTO_IPV6,
    IPV6_V6ONLY,
    error as SocketError,
    SOL_SOCKET,
    SO_REUSEADDR,
    SO_BROADCAST
)
import errno


class Dgram:
    def __init__(self, address: InternetAddress, is_server: bool):
        self.address: InternetAddress = address
        if address.version == 4:
            self.socket: Socket = Socket(
                AF_INET,
                SOCK_DGRAM,
                IPPROTO_UDP
            )
        elif address.version == 6:
            self.socket: Socket = Socket(
                AF_INET6,
                SOCK_DGRAM,
                IPPROTO_UDP
            )
            self.socket.setsockopt(
                IPPROTO_IPV6,
                IPV6_V6ONLY,
                1
            )
        else:
            raise InvalidAddressVersion(
                "Invalid version: " + str(address.version),
            )
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        if is_server:
            try:
                self.socket.bind((address.name, address.port))
            except SocketError as e:
                if e.errno == errno.EADDRINUSE:
                    raise PortInUse(
   	                str(address.port) + " already in use"
                    )
                else:
                    raise FailedToBindPort("Failed to bind")
        self.socket.setblocking(False)

    def receive(self) -> tuple:
        while True:
            try:
                return self.socket.recvfrom(0xffff)
            except BlockingIOError as e:
                return False

    def send(self, data: bytes, address: tuple) -> int:
        try:
            return self.socket.sendto(data, address)
        except BlockingIOError as e:
            return False
