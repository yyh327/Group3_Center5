import streamlit as st
import pandas as pd
import itertools

st.set_page_config(page_title="時間割", layout="wide")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

# タイトル表示（HTMLスタイルで補足付き）
st.markdown("""
### 🗓️ 教室別 時間割  
<span style='font-size: 1em; color: gray;'>(Classroom Timetable)</span>
""", unsafe_allow_html=True)

# 教室選択
st.markdown("""
### 🏫 教室を選んでください  
<span style='font-size: 1em; color: gray;'>(Please select a classroom)</span>
""", unsafe_allow_html=True)

# 教室リスト
floor_3_rooms = ['5301', '5302', '5303', '5304', '5305', '5306', '5307', '5308',
                 '5309', '5310', '5311', '5312', '5313']
floor_4_rooms = ['5401', '5402', '5403', '5404', '5405', '5406', '5407', '5408',
                 '5409', '5410', '5411', '5412', '5413', '5414', '5415', '5416', '5417']
all_rooms = sorted(floor_3_rooms + floor_4_rooms)

selected_room = st.selectbox("教室を選択 / Select classroom", all_rooms)

# データ前処理
df["Day"] = df["Day"].fillna("")
df["Period"] = df["Period"].fillna(0).astype(int)
df["Room"] = df["Room"].astype(str)

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
day_labels = {"Monday": "月", "Tuesday": "火", "Wednesday": "水", "Thursday": "木", "Friday": "金"}

# 教室の授業データ抽出
room_df = df[df["Room"] == selected_room].copy()

# 授業名と教員名をまとめて表示
room_df["Display"] = room_df["Class name"].fillna("") + "（" + room_df["Teacher"].fillna("") + "）"

# すべての曜日×時限の組み合わせを作成
all_periods = range(1, 6)  # 1〜5限
all_combinations = pd.DataFrame(list(itertools.product(all_periods, day_order)), columns=["Period", "Day"])

# 授業データとマージ
merged = pd.merge(all_combinations, room_df[["Period", "Day", "Display"]], on=["Period", "Day"], how="left")

# ピボットテーブルを作成
pivot = merged.pivot(index="Period", columns="Day", values="Display").fillna("")
pivot = pivot.reindex(columns=day_order).rename(columns=day_labels)
pivot.index.name = "時限"

# 色分け関数
def style_table(val):
    if val == "":
        return "background-color: #d4f4dd; text-align: center;"  # 空き：緑
    else:
        return "background-color: #f0f0f0; text-align: left;"    # 授業：灰色

# 時間割の表示
st.markdown(f"### 📋 {selected_room} の時間割 / {selected_room} Timetable")

st.dataframe(
    pivot.style.applymap(style_table),
    use_container_width=True,
    height=500
)
