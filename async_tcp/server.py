#!/usr/bin/env python3
"""TCP echo server example.
Based on code from:
https://github.com/python/asyncio/blob/master/examples/tcp_echo.py

See client.py to find out how to run the two.
"""

import argparse
import asyncio
import sys
try:
    import signal
except ImportError:
    signal = None


class EchoServer(asyncio.Protocol):
    """."""
    TIMEOUT = 5.0

    def __init__(self):
        self.h_timeout = None
        self.transport = None
        print("Server: created")

    def timeout(self):
        """ Close the connection when a timeout occurs."""
        print("Server: connection timeout, closing.")
        self.transport.close()

    def connection_made(self, transport):
        """ When a connection is made, store the transport of later use and
            start the timeout.
        """
        print("Server: connection made")
        self.transport = transport

        # start 5 seconds timeout timer
        self.h_timeout = asyncio.get_event_loop().call_later(
            self.TIMEOUT, self.timeout)

    def data_received(self, data):
        """."""
        print("Server: data received: '{0}'".format(data.decode()))
        self.transport.write(b"Re: " + data)

        # restart timeout timer
        self.h_timeout.cancel()
        self.h_timeout = asyncio.get_event_loop().call_later(
            self.TIMEOUT, self.timeout)

    def eof_received(self):
        """."""
        pass

    def connection_lost(self, exc):
        """."""
        print("Server: connection lost:", exc)
        self.h_timeout.cancel()


ARGS = argparse.ArgumentParser(description="TCP Echo example.")
ARGS.add_argument(
    "--host", action="store", dest="host",
    default="127.0.0.1", help="Host name")
ARGS.add_argument(
    "--port", action="store", dest="port",
    default=9999, type=int, help="Port number")


if __name__ == "__main__":
    ARGUMENTS = ARGS.parse_args()

    if ":" in ARGUMENTS.host:
        ARGUMENTS.host, PORT = ARGUMENTS.host.split(":", 1)
        ARGUMENTS.port = int(PORT)

    LOOP = asyncio.get_event_loop()
    print("Server: using backend: {0}".format(LOOP.__class__.__name__))

    if signal is not None and sys.platform != "win32":
        LOOP.add_signal_handler(signal.SIGINT, LOOP.stop)

    print("Server: starting")
    SERVER = LOOP.create_server(EchoServer, ARGUMENTS.host, ARGUMENTS.port)
    LOOP.run_until_complete(SERVER)

    try:
        print("Server: running")
        LOOP.run_forever()
    finally:
        SERVER.close()
        LOOP.close()
        print("Server: stopped")
