import asyncio
from random import randint

loop = asyncio.get_event_loop()
future = loop.create_future()

def random_hit(future, n, cnt=1, loop=None):
    #import pdb; pdb.set_trace()
    if loop is None:
        loop = asyncio.get_event_loop()
    v = randint(1, n)
    if v == 1:
        future.set_result(cnt)
    else:
        cnt += 1
        loop.call_soon(random_hit, future, n, cnt, loop)

future.add_done_callback(lambda f: print("done"))
loop.call_soon(random_hit, future, 100)

result = loop.run_until_complete(future)
print(result)

loop.close()
