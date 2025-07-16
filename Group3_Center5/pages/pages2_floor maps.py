import streamlit as st
import pandas as pd
from PIL import Image, ImageOps

st.set_page_config(page_title="センター5号館 教室検索", layout="wide")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

st.title("センター5号館 教室検索")

# --- 画面を左右に分割 ---
spacer_col, left_col, right_col = st.columns([0.1, 0.6, 0.3])


with left_col:
    # --- 1. 階数選択 ---
    floor_options = ["3F", "4F"]
    st.markdown("### 階数を選んでください")
    selected_floor = st.radio("", floor_options, horizontal=True)

    # --- 2. 教室リストと画像パス切り替え ---
    if selected_floor == "3F":
        image_path = "/mount/src/group3_center5/Group3_Center5/pages/5goukan3F.jpg"
        room_list = ['5301', '5302', '5303', '5304', '5305', '5306', '5307', '5308',
                     '5309', '5310', '5311', '5312', '5313']
    else:
        image_path = "/mount/src/group3_center5/Group3_Center5/pages/5goukan4F.jpg"
        room_list = ['5401', '5402', '5403', '5404', '5405', '5406', '5407', '5408',
                     '5409', '5410', '5411', '5412', '5413', '5414', '5415', '5416', '5417']

    # --- 3. 曜日選択 ---
    st.markdown("### 曜日を選んでください")
    days_jp = ["月", "火", "水", "木", "金"]
    day_mapping = {
        "Monday": "月", "Tuesday": "火", "Wednesday": "水", "Thursday": "木", "Friday": "金"
    }
    selected_day_jp = st.radio("", days_jp, horizontal=True)
    selected_day_en = [k for k, v in day_mapping.items() if v == selected_day_jp][0]

    # --- 4. 教室ボタン ---
    st.markdown("### 教室をクリックしてください")
    room_clicked = None
    cols = st.columns(3)

    for i, room in enumerate(room_list):
        if cols[i % 3].button(room):
            room_clicked = room

with right_col:
    # --- 地図画像の表示（向き補正あり） ---
    image = ImageOps.exif_transpose(Image.open(image_path))
    st.image(image, caption=f"センター5号館 {selected_floor}", width=400)

# --- 5. 授業表示（画面下に全体表示） ---
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
