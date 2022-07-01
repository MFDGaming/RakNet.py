"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

from raknet.misc.dgram import Dgram
from raknet.misc.internet_address import InternetAddress
from time import time
from math import floor
from random import randint
from sys import maxsize
from typing import Callable


class Sc:
    def __init__(
        self,
        address: InternetAddress,
        protocol_version: int,
        is_server: bool
    ):
        self.address: InternetAddress = address
        self.protocol_version: int = protocol_version
        self.epoch: int = floor(time() * 1000)
        self.guid: int = randint(0, maxsize)
        self.is_running: bool = True
        self.dgram = Dgram(self.address, is_server)
        self.message: str = ""
        self.system_addresses_count: int = 20
        self.connected_handler: Callable = lambda connection: None
        self.frame_handler: Callable = lambda frame, connection: None
        self.disconnected_handler = lambda connection: None
        self.connected_pong_has_pong_timestamp: bool = True

    @property
    def timestamp(self) -> int:
        return floor(time() * 1000) - self.epoch
