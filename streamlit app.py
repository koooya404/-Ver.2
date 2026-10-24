"""単語ガチャ(Streamlit版・Googleスプレッドシート連動)

シートのA列に単語を1行ずつ書くだけ(1行目は見出し)。
シートの共有設定は「リンクを知っている全員が閲覧可」にしてください。
"""
import csv
import io
import random
import urllib.request

import streamlit as st

SHEET_ID = "1-VlnFIsUMX9O8c7UoKPwNiLqY-XpwTdeH8XgbJLm0e4"
GID = 0
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
COUNT = 3  # 1回で引く単語数

st.set_page_config(page_title="単語ガチャ", layout="centered")

# 背景を白、文字を黒に固定(端末のダークモードでも変わらない)
st.markdown(
    """
    <style>
    .stApp, header[data-testid="stHeader"] { background: #ffffff; }
    .stApp, .stApp * { color: #000000; }
    .stButton > button {
        background: #ffffff; border: 2px solid #000000; border-radius: 8px;
        font-size: 1.4rem; font-weight: 700; padding: 0.6rem 2rem;
    }
    .stButton > button:hover, .stButton > button:active {
        background: #eeeeee; border-color: #000000;
    }
    .word { font-size: 2rem; text-align: center; margin: 0.6rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_words():
    """A列の単語を読む。空行・重複登録は除く。"""
    text = urllib.request.urlopen(URL, timeout=15).read().decode("utf-8")
    rows = list(csv.reader(io.StringIO(text)))[1:]  # 1行目は見出し
    words = [r[0].strip() for r in rows if r and r[0].strip()]
    return list(dict.fromkeys(words))


st.markdown("<h1 style='text-align:center'>単語ガチャ</h1>", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 2, 1])
with mid:
    pulled = st.button("ガチャを引く！", use_container_width=True)

if pulled:
    try:
        words = load_words()
    except Exception:
        st.error("シートを読み込めませんでした。共有設定が「リンクを知っている全員が閲覧可」か確認してください。")
    else:
        if not words:
            st.warning("単語がありません。シートのA列(2行目以降)に入力してください。")
        else:
            for w in random.sample(words, k=min(COUNT, len(words))):  # 重複なし
                st.markdown(f"<div class='word'>{w}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='word'>ボタンを押してください</div>", unsafe_allow_html=True)
