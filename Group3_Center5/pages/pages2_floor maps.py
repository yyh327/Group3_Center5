import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Floor Maps")

# ヘッダー
st.markdown("## Floor Maps")
st.sidebar.header("Floor Maps")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

st.title("センター5号館 曜日別・教室別時間割")

# --- 地図画像表示 ---
st.subheader("5号館3F 教室マップ")
image = Image.open("pages/5goukan3F.jpg")  # 画像パスを適宜調整
st.image(image, use_column_width=True)

# --- 曜日選択 ---
day_mapping = {
    "Monday": "月",
    "Tuesday": "火",
    "Wednesday": "水",
    "Thursday": "木",
    "Friday": "金"
}
days_jp = ["月", "火", "水", "木", "金"]
selected_day_jp = st.radio("曜日を選んでください", days_jp, horizontal=True)
selected_day_en = [k for k, v in day_mapping.items() if v == selected_day_jp][0]

# --- 教室名ボタンで選択 ---
st.subheader("教室をクリックして選んでください")

# ボタン（教室名）を横並びで表示
cols = st.columns(4)  # 4列に分ける

room_clicked = None
room_list = df["Room"].unique()

for i, room in enumerate(room_list):
    if cols[i % 4].button(room):
        room_clicked = room

# --- 授業表示 ---
if room_clicked:
    st.success(f"{room_clicked} を選択しました")
    filtered = df[(df["Day"] == selected_day_en) & (df["Room"] == room_clicked)]
    if not filtered.empty:
        display_df = filtered[["Room", "Class name", "Teacher", "Period"]].copy()
        display_df.columns = ["教室", "授業名", "担当教員", "時限"]
        display_df = display_df.sort_values("時限")
        st.table(display_df)
    else:
        st.info(f"{selected_day_jp}曜日の{room_clicked}の授業は登録されていません。")
else:
    st.info("地図を見て教室名をクリックしてください。")
