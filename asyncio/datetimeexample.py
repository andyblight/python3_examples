"""Example taken from
https://docs.python.org/3/library/asyncio-task.html#example-coroutine-displaying-the-current-date.
Sorted out PyLint warnings."""
import asyncio
import datetime

@asyncio.coroutine
def display_date(loop):
    """Prints the time and date once a second for 5 seconds."""
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        yield from asyncio.sleep(1)

LOOP = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
LOOP.run_until_complete(display_date(LOOP))
LOOP.close()
