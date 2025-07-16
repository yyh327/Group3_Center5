import streamlit as st
import pandas as pd
from PIL import Image, ImageOps

st.set_page_config(page_title="センター5号館 時間割マップ", layout="wide")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

st.title("センター5号館 フロアマップ ＋ 授業時間割")

# --- 1. 階数選択 ---
floor_options = ["3F", "4F"]
selected_floor = st.radio("階数を選んでください", floor_options, horizontal=True)

# --- 2. フロアマップ画像（左右に並べて表示） ---
col1, col2 = st.columns(2)

# 各階の画像読み込みと向き補正
image_3f = ImageOps.exif_transpose(Image.open("/mount/src/group3_center5/Group3_Center5/pages/5goukan3F.jpg"))
image_4f = ImageOps.exif_transpose(Image.open("/mount/src/group3_center5/Group3_Center5/pages/5goukan4F.jpg"))

with col1:
    st.image(image_3f, caption="センター5号館 3F", width=400)
with col2:
    st.image(image_4f, caption="センター5号館 4F", width=400)

# --- 3. 曜日選択 ---
st.markdown("### 曜日を選んでください")
days_jp = ["月", "火", "水", "木", "金"]
day_mapping = {
    "Monday": "月", "Tuesday": "火", "Wednesday": "水", "Thursday": "木", "Friday": "金"
}
selected_day_jp = st.radio("", days_jp, horizontal=True)
selected_day_en = [k for k, v in day_mapping.items() if v == selected_day_jp][0]

# --- 4. 教室リスト（階によって分岐） ---
room_list_3f = ['5301', '5302', '5303', '5304', '5305', '5306', '5307', '5308', '5309', '5310', '5311', '5312', '5313']
room_list_4f = ['5401', '5402', '5403', '5404', '5405', '5406', '5407', '5408', '5409', '5410', '5411', '5412', '5413', '5414', '5415', '5416', '5417']

room_list = room_list_3f if selected_floor == "3F" else room_list_4f

# --- 5. 教室選択ボタン ---
st.markdown("### 教室をクリックしてください")
room_clicked = None
cols = st.columns(5)

for i, room in enumerate(room_list):
    if cols[i % 5].button(room):
        room_clicked = room

# --- 6. 授業表示 ---
if room_clicked:
    st.success(f"{selected_floor} {room_clicked} を選択しました（{selected_day_jp}曜日）")
    filtered = df[
        (df["Day"] == selected_day_en) &
        (df["Room"].astype(str) == room_clicked)
    ]
    if not filtered.empty:
        display_df = filtered[["Room", "Class name", "Teacher", "Period"]].copy()
        display_df.columns = ["教室", "授業名", "担当教員", "時限"]
        display_df = display_df.sort_values("時限")
        st.table(display_df)
    else:
        st.info(f"{selected_day_jp}曜日の {room_clicked} の授業は登録されていません。")
