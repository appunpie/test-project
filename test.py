import sys
import time
import json
import requests

# グローバル変数
cache = {}  # 関数f(seed, n)で何度も呼び出されることを避けるために一度計算した結果は格納しておき、次に同じ処理を求められたときはここから結果を引っ張り出す
api_call_timestamps = []  # APIサーバーにアクセスしたときの時間を格納する
CALL_LIMIT = 50  # 呼び出し回数を50回に制限する
TIME_WINDOW = 3600  # 1時間 = 3600秒

# API呼び出し制限を確認
# この関数は固定のseed値に対して、呼び出す回数を制限するものではなく、どんなseed値であっても1時間にアクセスできる回数を50回に制限してしまう関数になってしまいました。
def can_call_api():
    now = time.time()  # APIにアクセスしたときの現在時刻を取得
    global api_call_timestamps  # グローバル変数を使用することを宣言
    api_call_timestamps = [t for t in api_call_timestamps if now - t < TIME_WINDOW]  # 現在時刻から一時間前のtimestampはリストから削除する
    if len(api_call_timestamps) < CALL_LIMIT:  # アクセス回数の制限を超えていない場合、新たなtimestampを追加する
        api_call_timestamps.append(now)
        return True
    return False

# API呼び出し
def askServer(n, seed):
    # まず、can_call_apiでアクセスができるかどうかを判断する
    if not can_call_api():
        print("503 Service Unavailable")  # できない場合はエラーを返す
        sys.exit(1)

    try:  # GETメソッドでリクエストを送った場合の処理をいかに記述した
        response = requests.get(
            "http://challenge-server.code-check.io/api/recursive/ask",
            params={"seed": seed, "n": n}
        )
    except requests.exceptions.RequestException:
        print("503 Service Unavailable")
        sys.exit(1)

    if response.status_code == 200:
        raw_result = response.json()["result"]
        result = (raw_result % 300) + 1  # APIサーバーから受け取った値を1から300以内の数字に変換する
        return result
    elif response.status_code == 503:
        print("503 Service Unavailable")
        sys.exit(1)
    else:
        print(f"{response.status_code} {response.reason}")
        sys.exit(1)

# 再帰関数
def f(n, seed):
    # 一度計算が行われた関数がcashe内にあるなら、その値をcasheから渡す
    if n in cache:
        return cache[n]

    if n == 0:
        result = 1
    elif n == 2:
        result = 2
    elif n % 2 == 0:
        result = (
            f(n - 1, seed) +
            f(n - 2, seed) +
            f(n - 3, seed) +
            f(n - 4, seed)
        )
    else:
        result = askServer(n, seed)

    cache[n] = result
    return result

# メイン関数
def main():
    # そもそも与えられた値の数が不足していたり、余分な値が記載されていた場合
    if len(sys.argv) != 3:
        print("400 BadRequest")
        sys.exit(1)

    seed = sys.argv[1]
    try:
        # int型に変換できない場合、数字意外の文字が含まれており、エラー対象となる
        #もう一つ加える条件として1<= n <= 50があると尚よいのかもしれない
        n = int(sys.argv[2])  
    except ValueError:
        print("400 BadRequest")
        sys.exit(1)

    try:
        result = f(n, seed)
        print("200 OK")
        # 正常に処理されたときにseed, n, resultをJSON形式で出力する
        print(json.dumps({
            "seed": seed,
            "n": n,
            "result": result
        }))
    except Exception:
        print("503 Service Unavailable")
        sys.exit(1)

if __name__ == "__main__":
    main()
