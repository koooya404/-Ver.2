"""単語ガチャ(画面付き・Googleスプレッドシート版)

シートのA列に単語を1行ずつ書くだけ(1行目は見出し)。
シートの共有設定は「リンクを知っている全員が閲覧可」にしてください。

使い方:
    python word_gacha_gui.py
「ガチャを引く！」ボタンを押すと単語が表示されます。
1回の抽選では同じ単語は出ません。ボタンを押すたびにシートを読み直すので、
単語を足せばすぐ反映されます。
"""
import csv
import io
import random
import tkinter as tk
import urllib.request

SHEET_ID = "1-VlnFIsUMX9O8c7UoKPwNiLqY-XpwTdeH8XgbJLm0e4"
GID = 0
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
COUNT = 3  # 1回で引く単語数

BG = "#ffffff"  # 背景: 白
FG = "#000000"  # 文字: 黒
FONT = ("Yu Gothic UI", 20)


def load_words():
    """A列の単語を読む。空行・重複登録は除く。"""
    text = urllib.request.urlopen(URL, timeout=15).read().decode("utf-8")
    rows = list(csv.reader(io.StringIO(text)))[1:]  # 1行目は見出し
    words = [r[0].strip() for r in rows if r and r[0].strip()]
    return list(dict.fromkeys(words))


def pull():
    """ボタンが押されたときの処理: 単語を引いて画面に表示する。"""
    try:
        words = load_words()
    except Exception:
        result.set("シートを読み込めませんでした。\n共有設定が「リンクを知っている全員が閲覧可」か\n確認してください。")
        return
    if not words:
        result.set("単語がありません。\nシートのA列(2行目以降)に入力してください。")
        return
    picks = random.sample(words, k=min(COUNT, len(words)))  # 重複なし
    result.set("\n".join(picks))


root = tk.Tk()
root.title("単語ガチャ")
root.configure(bg=BG)
root.geometry("420x360")

result = tk.StringVar(value="ボタンを押してください")

tk.Label(root, text="単語ガチャ", font=("Yu Gothic UI", 26, "bold"),
         bg=BG, fg=FG).pack(pady=(24, 12))

tk.Button(root, text="ガチャを引く！", font=("Yu Gothic UI", 18, "bold"),
          bg=BG, fg=FG, activebackground="#eeeeee", activeforeground=FG,
          relief="solid", bd=2, padx=24, pady=8, command=pull).pack(pady=12)

tk.Label(root, textvariable=result, font=FONT, bg=BG, fg=FG,
         justify="center").pack(expand=True, pady=12)

root.mainloop()
