"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

class Identifiers:
    UNCONNECTED: dict = {
        "UNCONNECTED_PING": 0x01,
        "UNCONNECTED_PING_OPEN_CONNECTIONS": 0x02,
        "UNCONNECTED_PONG": 0x1c,
        "OPEN_CONNECTION_REQUEST_ONE": 0x05,
        "OPEN_CONNECTION_REPLY_ONE": 0x06,
        "OPEN_CONNECTION_REQUEST_TWO": 0x07,
        "OPEN_CONNECTION_REPLY_TWO": 0x08,
        "INCOMPATIBLE_PROTOCOL_VERSION": 0x19,
        "ACK": 0xc0,
        "NACK": 0xa0,
        "FRAME_SET_0": 0x80,
        "FRAME_SET_1": 0x81,
        "FRAME_SET_2": 0x82,
        "FRAME_SET_3": 0x83,
        "FRAME_SET_4": 0x84,
        "FRAME_SET_5": 0x85,
        "FRAME_SET_6": 0x86,
        "FRAME_SET_7": 0x87,
        "FRAME_SET_8": 0x88,
        "FRAME_SET_9": 0x89,
        "FRAME_SET_A": 0x8a,
        "FRAME_SET_B": 0x8b,
        "FRAME_SET_C": 0x8c,
        "FRAME_SET_D": 0x8d,
        "FRAME_SET_E": 0x8e,
        "FRAME_SET_F": 0x8f
    }

    CONNECTED: dict = {
        "CONNECTED_PING": 0x00,
        "CONNECTED_PONG": 0x03,
        "CONNECTION_REQUEST": 0x09,
        "CONNECTION_REQUEST_ACCEPTED": 0x10,
        "NEW_INCOMING_CONNECTION": 0x13,
        "DISCONNECT_NOTIFICATION": 0x15
    }
