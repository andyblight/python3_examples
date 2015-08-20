#!/usr/bin/env python3
"""TCP echo client example.
Based on code from:
https://github.com/python/asyncio/blob/master/examples/tcp_echo.py

Invoke as follows:
./server.py &
Server: using backend: _UnixSelectorEventLoop
Server: starting
Server: running
./client.py
Client: starting
Server: created
Server: connection made
Client: data sent: 'This is the MESSAGE. It will be echoed.'
Client: running
Server: data received: 'This is the MESSAGE. It will be echoed.'
Client: data received: 'b'Re: This is the MESSAGE. It will be echoed.'
Server: connection timeout, closing.
Server: connection lost: None
Client: connection lost: None
Client: stopped

"""

import argparse
import asyncio
import sys
try:
    import signal
except ImportError:
    signal = None


class EchoClient(asyncio.Protocol):
    """."""
    MESSAGE = "This is the MESSAGE. It will be echoed."

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        """."""
        self.transport = transport
        self.transport.write(self.MESSAGE.encode())
        print("Client: data sent: '{0}'".format(self.MESSAGE))

    def data_received(self, data):
        """."""
        print("Client: data received: '{0}".format(data))

        # disconnect after 10 seconds
        asyncio.get_event_loop().call_later(10.0, self.transport.close)

    def eof_received(self):
        """."""
        pass

    def connection_lost(self, exc):
        """."""
        print("Client: connection lost:", exc)
        asyncio.get_event_loop().stop()


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
    if signal is not None and sys.platform != "win32":
        LOOP.add_signal_handler(signal.SIGINT, LOOP.stop)

    print("Client: starting")
    TASK = asyncio.Task(LOOP.create_connection(EchoClient,
                                               ARGUMENTS.host, ARGUMENTS.port))
    LOOP.run_until_complete(TASK)

    try:
        print("Client: running")
        LOOP.run_forever()
    finally:
        LOOP.close()
        print("Client: stopped")
