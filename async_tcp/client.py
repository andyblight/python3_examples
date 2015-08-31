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
    """Sends a message to the server and prints out what is sent back."""

    MESSAGE = "This is the MESSAGE. It will be echoed."

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        """Sends the message when the connection is made."""
        self.transport = transport
        self.transport.write(self.MESSAGE.encode())
        print("Client: data sent: '{0}'".format(self.MESSAGE))

    def data_received(self, data):
        """Print out data and close after 10 seconds."""
        print("Client: data received: '{0}".format(data))
        # disconnect after 10 seconds
        asyncio.get_event_loop().call_later(10.0, self.transport.close)

    def eof_received(self):
        """Ignore EOF."""
        pass

    def connection_lost(self, exc):
        """Stop client when the connection is lost."""
        print("Client: connection lost:", exc)
        asyncio.get_event_loop().stop()


def main():
    """Setup and run the application."""
    # Parse the arguments passed to the application
    args = argparse.ArgumentParser(description="TCP Echo example client.")
    args.add_argument(
        "--host", action="store", dest="host",
        default="127.0.0.1", help="Host name")
    args.add_argument(
        "--port", action="store", dest="port",
        default=9999, type=int, help="Port number")
    arguments = args.parse_args()
    if ":" in arguments.host:
        arguments.host, PORT = arguments.host.split(":", 1)
        arguments.port = int(PORT)

    # Start the main loop
    loop = asyncio.get_event_loop()
    if signal is not None and sys.platform != "win32":
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    print("Client: starting")
    task = asyncio.Task(loop.create_connection(EchoClient,
                                               arguments.host, arguments.port))
    loop.run_until_complete(task)

    try:
        print("Client: running")
        loop.run_forever()
    finally:
        loop.close()
        print("Client: stopped")

if __name__ == "__main__":
    main()
