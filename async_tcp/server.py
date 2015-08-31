#!/usr/bin/env python3
"""TCP echo server example.
Based on code from:
https://github.com/python/asyncio/blob/master/examples/tcp_echo.py

See client.py to find out how to run the two examples.
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
        """Print out the received data and echo it back."""
        print("Server: data received: '{0}'".format(data.decode()))
        self.transport.write(b"Re: " + data)

        # restart timeout timer
        self.h_timeout.cancel()
        self.h_timeout = asyncio.get_event_loop().call_later(
            self.TIMEOUT, self.timeout)

    def eof_received(self):
        """Ignore EOF."""
        pass

    def connection_lost(self, exc):
        """Cancel the time out when the connection has been lost."""
        print("Server: connection lost:", exc)
        self.h_timeout.cancel()

def main():
    """Setup and run the application."""
    # Parse the arguments passed to the application
    args = argparse.ArgumentParser(description="TCP Echo example.")
    args.add_argument(
        "--host", action="store", dest="host",
        default="127.0.0.1", help="Host name")
    args.add_argument(
        "--port", action="store", dest="port",
        default=9999, type=int, help="Port number")
    arguments = args.parse_args()
    if ":" in arguments.host:
        arguments.host, port = arguments.host.split(":", 1)
        arguments.port = int(port)

    # Run the application.
    loop = asyncio.get_event_loop()
    print("Server: using backend: {0}".format(loop.__class__.__name__))
    if signal is not None and sys.platform != "win32":
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    print("Server: starting")
    server = loop.create_server(EchoServer, arguments.host, arguments.port)
    loop.run_until_complete(server)

    try:
        print("Server: running")
        loop.run_forever()
    finally:
        server.close()
        loop.close()
        print("Server: stopped")

if __name__ == "__main__":
    main()
