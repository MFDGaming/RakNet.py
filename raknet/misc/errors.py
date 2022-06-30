"""
   Copyright Alexander Argentakis
   Repo: https://github.com/MFDGaming/RakNet.py
   This file is licensed under the GPL v2.0 license
"""

class InvalidAddressVersion(Exception):
    pass

class InvalidPort(Exception):
    pass

class PortInUse(Exception):
    pass

class FailedToBindPort(Exception):
    pass

class InvalidMagic(Exception):
    pass
