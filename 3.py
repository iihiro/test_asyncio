import asyncio

'''
コルーチンとタスクの理解

asyncioで非同期処理を行う際の、"処理"を表す型としては以下の3つがある

* コルーチン
* Future
* Task

ここではコルーチンの理解とタスクとの関係を整理する
'''

loop = asyncio.get_event_loop()

# async def ...でコルーチンを定義できる
# これは関数ではなく、コルーチン
#
# コルーチンとは、awaitが書ける関数であり、
# 待ちが発生する箇所をawaitで示すことができる関数
# コルーチンの中に"await 処理"があると、そのタイミングで
# asyncioのスケジューラは既に登録済みの別の処理に切り替える
# そして、awaitで指定した処理が完了したらまた、戻る
# 処理が完了したことをどうやって知るかというと、
# "await 処理"の処理の部分にはFutureオブジェクトを指定できる
# Futureオブジェクトの add_done_callback() で元の処理の
# 再開したい部分以降を実行する関数を登録することで、
# "戻る"を実現しているはず
async def coro(str):
    print("hello, %s" % (str))

# コルーチンをイベントループへ登録するやり方は2つ

# 1. コルーチンをラップしたTaskオブジェクトを生成し、さらにイベントループへそのTaskオブジェクトを登録
#task = loop.create_task(coro("hoge")) # コルーチンをラップしたTaskオブジェクトを生成, コルーチンのみ渡せる
task = asyncio.ensure_future(coro("hoge")) # 同上(python3.xの初期ではこちら), コルーチンの他にFutureオブジェクトの渡せる
                                   # Futureオブジェクトを渡した場合は、*Taskオブジェクトではなく、Futureオブジェクトがそのまま返る*

# 2. run_until_completeへコルーチンをそのまま渡して、
# run_until_completeの内部でensure_futureが呼ばれて、
# 暗黙的にTaskオブジェクト(or Futureオブジェクトの結果がセットされるまで実行するという処理に変換されて)
# イベントループへ登録し、さらにイベントループを実行する
# ※TaskはFutureのサブクラスであるため、run_until_complete的には、TaskオブジェクトもFutureオブジェクトと同様に
# 「Taskオブジェクトの結果がセットされるまで実行するという処理」
loop.run_until_complete(coro("hoge2"))



