#! /usr/bin/python3
"""Asyncio exmaple.

Original code from
https://docs.python.org/3/library/asyncio-task.html#example-hello-world-coroutine.
Fixed PyLint warnings.
"""

import asyncio

@asyncio.coroutine
def hello_world():
    """Print Hello World."""
    print("Hello World!")

LOOP = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
LOOP.run_until_complete(hello_world())
LOOP.close()
