import asyncio

loop = asyncio.get_event_loop()

async def coro(id, f, loop):
    print("begin coro#%d" % (id))
    await f
    print("end coro#%d" % (id))
    if id == 2:
        loop.call_soon(loop.stop) # id2が終わったら、イベントループを止める

async def coro_no_await(id):
    print("begin coro#%d" % (id))
    print("end coro#%d" % (id))


loop.call_soon(lambda : print("hoge")) # 処理1. 通常関数を登録
future1 = loop.create_future()
future2 = loop.create_future()
asyncio.ensure_future(coro(1, future1, loop)) # 処理2. Task登録(future1の結果を待つawait有り)
asyncio.ensure_future(coro(2, future2, loop)) # 処理3. Task登録(future2の結果を待つawait有り)
asyncio.ensure_future(coro_no_await(3)) # 処理4. Task登録(await無し)

loop.call_later(1, lambda f: f.set_result("done"), future1) # 処理5. 通常関数登録(1秒後にfuture1の結果をセットする)
loop.call_later(2, lambda f: f.set_result("done"), future2) # 処理6. 通常関数登録(2秒後にfuture2の結果をセットする)

loop.run_forever()
loop.close()
