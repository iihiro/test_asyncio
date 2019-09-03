import asyncio
import datetime


def display_date(end_time, loop):
    print(datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.call_soon(loop.stop)

def display_date2(loop):
    print(datetime.datetime.now())
    try:
        loop.call_later(1, display_date2, loop)
    except KeyboardInterrupt:
        loop.stop()

loop = asyncio.get_event_loop()

end_time = loop.time() + 5.0
#loop.call_soon(display_date, end_time, loop)
loop.call_soon(display_date2, loop)

loop.run_forever()
loop.close()
