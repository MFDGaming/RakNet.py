"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

class Reliability:
    UNRELIABLE: int = 0
    UNRELIABLE_SEQUENCED: int = 1
    RELIABLE: int = 2
    RELIABLE_ORDERED: int = 3
    RELIABLE_SEQUENCED: int = 4
    UNRELIABLE_WITH_ACK_RECEIPT: int = 5
    RELIABLE_WITH_ACK_RECEIPT: int = 6
    RELIABLE_ORDERED_WITH_ACK_RECEIPT: int = 7
