import streamlit as st
import pandas as pd

st.set_page_config(page_title="時間割", layout="wide")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

st.title("🗓️ 教室別 時間割")

# --- 教室リスト選択 ---
st.markdown("### 🏫 教室を選んでください")

floor_3_rooms = ['5301', '5302', '5303', '5304', '5305', '5306', '5307', '5308',
                 '5309', '5310', '5311', '5312', '5313']
floor_4_rooms = ['5401', '5402', '5403', '5404', '5405', '5406', '5407', '5408',
                 '5409', '5410', '5411', '5412', '5413', '5414', '5415', '5416', '5417']
all_rooms = sorted(floor_3_rooms + floor_4_rooms)

selected_room = st.selectbox("教室を選択", all_rooms)

# --- データ処理 ---
df["Day"] = df["Day"].fillna("")
df["Period"] = df["Period"].fillna(0).astype(int)

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
day_labels = {"Monday": "月", "Tuesday": "火", "Wednesday": "水", "Thursday": "木", "Friday": "金"}

# 教室ごとのデータ抽出
room_df = df[df["Room"].astype(str) == selected_room]

# ピボットテーブル形式（曜日 × 時限）
pivot = room_df.pivot_table(index="Period", columns="Day", values="Class name", aggfunc=lambda x: " / ".join(x)).fillna("")

# 列順を整理 & ラベル変更
pivot = pivot.reindex(columns=day_order).rename(columns=day_labels)
pivot.index.name = "時限"

st.markdown(f"### 📋 {selected_room} の時間割")
st.table(pivot)
