import asyncio

'''
Futureオブジェクトの理解

asyncioで非同期処理を行う際の、"処理"を表す型としては以下の3つがある

* コルーチン
* Future
* Task

この内、TaskはFutureのサブクラスであるため、
一般的にはより抽象度の高いTaskを使うことが多く、そういった意味では
コルーチンとTaskとなる
ただし、コルーチンも結局Taskに変換されて扱われるため、そうするとTaskだけが残る
ただ、Taskは前述のとおりFutureのサブクラスであるため、まずはFutureを理解することが、
asyncioで非同期処理を行う際の基本でのデータ型を理解することとなる
'''

def func(str):
    print("hello, %s" % (str))


loop = asyncio.get_event_loop()

# Futureオブジェクトは以下のI/Fで作れる
# loopのAPIから作っていることから、Futureオブジェクトはイベントループ内部で
# 管理されているはず
#
# Futureは状態とそれに対するコールバックだけを持つシンプルなデータ構造
# 名前の由来は、まだ状態が完了になっていなくても投機的に扱える(="未来"を扱える)ことからきているのではと推測
# 要は、内部で処理が終わった、終わってないという状態(結果)を持っていて、外部からその状態をset, getできて、
# 予め、"状態がセットされたときのコールバック"を登録しておくと、その時にそれがコールバックされる、
# という感じのオブジェクト
future = loop.create_future()

# イベントループへ2つの関数を登録
loop.call_soon(func, "hoge") # 処理1(通常関数)
loop.call_soon(func, "fuga") # 処理2(通常関数)

# Futureオブジェクトに結果をセットする関数をイベントループへ登録
def set_result(v, f):
    if not f.done():
        f.set_result(v)
loop.call_soon(set_result, "done", future) # 処理3(通常関数)

# Futureオブジェクトに結果がセットされたときのコールバックを設定する
# コールバック関数は func(future) の型である必要がある
def callback(f):
    print("callback")
#future.add_done_callback(callback)
future.add_done_callback(lambda f: print("callback"))

# run_until_completeはすでにイベントループへ登録済みの処理に加えて、
# run_until_completeの引数で渡される処理を追加でイベントループへ登録(おそらく、内部的にはcall_soon()で登録)
# して、さらに"登録された処理がすべて完了するまで実行する"という動作を行う
# より正確には、登録された処理がすべて完了したら、loop.stop()をcall_soon()で登録する
#
# run_until_completeの引数でFutureオブジェクトが渡された場合には、
# イベントループへ登録される処理としては、"「Futureオブジェクトの結果がセットされるまで実行する」という処理"が
# 登録される
#
# 以上のことから、実際に以下のrun_until_completeでは、
# シーケンシャルに、処理1→2→3と実行され、
# それと平行して、処理4が実行される
# 処理4は処理3により、set_resultされると、その結果を返して処理を終える
loop.run_until_complete(future) # 処理4(Task)
