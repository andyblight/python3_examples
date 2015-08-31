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

def main():
    """Run the application."""
    loop = asyncio.get_event_loop()
    # Blocking call which returns when the hello_world() coroutine is done
    loop.run_until_complete(hello_world())
    loop.close()

if __name__ == "__main__":
    main()
