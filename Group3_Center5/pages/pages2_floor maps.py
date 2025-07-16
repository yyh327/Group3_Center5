import streamlit as st
import pandas as pd
from PIL import Image, ImageOps

st.set_page_config(page_title="Floor Maps")

# ヘッダー
st.markdown("## Floor Maps")
st.sidebar.header("Floor Maps")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

st.title("センター5号館 曜日別・教室別時間割")


# 地図画像表示
image = Image.open("/mount/src/group3_center5/Group3_Center5/pages/5goukan3F.jpg")
image = ImageOps.exif_transpose(image) 
st.image(image, caption="センター5号館 3F 教室案内", width=400)


# 曜日選択
day_mapping = {
    "Monday": "月", "Tuesday": "火", "Wednesday": "水", "Thursday": "木", "Friday": "金"
}
days_jp = ["月", "火", "水", "木", "金"]
st.subheader("曜日を選んでください")
selected_day_jp = st.radio("", days_jp, horizontal=True)
selected_day_en = [k for k, v in day_mapping.items() if v == selected_day_jp][0]

# 教室ボタン
st.subheader("教室をクリックしてください")
room_list = ['5301', '5302', '5303', '5304', '5305', '5306', '5307', '5308', '5309', '5310', '5311', '5312', '5313']
room_clicked = None
cols = st.columns(5)

for i, room in enumerate(room_list):
    if cols[i % 5].button(room):
        room_clicked = room

# 授業表示
if room_clicked:
    st.success(f"{room_clicked} を選択しました（{selected_day_jp}曜日）")
    filtered = df[(df["Day"] == selected_day_en) & (df["Room"].astype(str) == room_clicked)]
    if not filtered.empty:
        display_df = filtered[["Room", "Class name", "Teacher", "Period"]].copy()
        display_df.columns = ["教室", "授業名", "担当教員", "時限"]
        display_df = display_df.sort_values("時限")
        st.table(display_df)
    else:
        st.info(f"{selected_day_jp}曜日の {room_clicked} の授業は登録されていません。")

