import asyncio

'''
イベントループに関数を登録して実行する

asyncioの基本は、イベントループに処理を登録して実行すること
プログラマは登録を行い、実行の部分はasyncioのスケジューラに任せることになる

以下の例では、イベントループへ通常の関数を登録して実行させている
ただし、通常の関数を登録した場合、asyncioの本来の目的である非同期処理は行われない
'''

def func(str):
    print("hello, %s" % (str))

# イベントループ作成
# 初回のasyncio.get_event_loop()で、このスレッドに唯一となるイベントループを取得する。
# 実際は、メインスレッドに対してシングルトンなイベントループスレッドが生成されているはず。
# このスレッドは、asyncioをインポートしたpythonスクリプトが実装された時に、
# はじめのインポードで生成されているはず。
# その後、同一スレッド内でasyncio.get_event_loop()を何度読んでも作成済みの同じイベントループが返される
# loop.close()でこのスレッドは破棄され、asyncio.new_event_loop()で作成できる
loop = asyncio.get_event_loop()

# call_soon()ですぐに実行する処理をイベントループへ登録できる
# ただし、登録だけなので実行はされない
# 実行は、loop.run_*したタイミング
loop.call_soon(func, "hoge")

# call_later()でN秒後に実行する処理をイベントループへ登録できる
loop.call_later(2, func, "fuga")

# イベントループを止める(中断する)場合は、loop.stopを処理として登録してやればよい
# loop.stopが呼ばれると、その時点でイベントループへ登録されている全ての処理を終わらせてから、
# イベントループを中断する。このとき、上記のcall_later(2, ..)は、実装上以下のようになっているので、
#
# call_later(time, f, args):
#   sleep(1sec)
#   time -= 1
#   if time > 0:
#     call_later(time, f, args)
#   else:
#     f()
#
# 何度目かの再帰呼び出しの途中で中断されるような形になる
loop.call_soon(loop.stop)

# call_soon()やcall_laterはハンドルクラスのインスタンスを返す
# ハンドルクラスのcancel()で登録した処理をキャンセルできる
h2 = loop.call_soon(func, "hoge2")
print(h2) # -> <Handle func('hoge2') at 1.py:3>
h2.cancel()

# run_forever()で登録した処理を永遠に実行できる。
# 永遠とは、一通り実行し終わると、また始めから実行する、を繰り返すということ
# はじめに登録した処理を実行し、それが終わったら次に登録した処理、…となる。
# 登録した順番ではなく、"一斉"に処理を実行したい場合は、通常の関数ではなく、タスクを登録する必要がある
# 
# 今回は関数を登録しているため、上記の例では、
#   1. loop.call_soon(func, "hoge")
#   2. loop.call_later(2, func, "fuga")
#   3. loop.call_soon(loop.stop)
# の順となる。
# ただし、loop.call_later()については、内部で再帰呼出が
# 発生するため、実際は以下のようになる。
# 
#   1. loop.call_soon(func, "hoge")
#   2. loop.call_later(2, func, "fuga")
#      -> sleep(1)
#      -> loop.call_later(1, func, "fuga")を新規登録(-> 4.)
#   3. loop.call_soon(loop.stop)
#   4. loop.call_later(1, func, "fuga")
#      -> sleep(1)
#      -> loop.call_soon(func, "fuga")を新規登録(-> 5.)
#   5. loop.call_soon(func, "fuga")
# 
# つまり、この例だと3.でループが止まってしまうため、
# 結果的にloop.call_later(2, func, "fuga")は実行されない。
#
loop.run_forever()

# イベントループを閉じる
# これで、そのスレッドの唯一のイベントループが破棄される
loop.close()
