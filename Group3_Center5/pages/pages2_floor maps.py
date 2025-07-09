import streamlit as st
st.set_page_config(page_title="Floor Maps")

st.markdown("Floor Maps")
st.sidebar.header("Floor Maps")


import streamlit as st
import pandas as pd

# CSV読み込み（Shift-JIS対応）
df = pd.read_csv("data.csv", encoding="shift_jis")

st.title("センター5号館 3F 曜日別・教室別時間割")

# 曜日変換マップ（英語⇔日本語）
day_mapping = {
    "Monday": "月",
    "Tuesday": "火",
    "Wednesday": "水",
    "Thursday": "木",
    "Friday": "金"
}
days_jp = ["月", "火", "水", "木", "金"]

# 曜日選択UI
selected_day_jp = st.radio("曜日を選んでください", days_jp, horizontal=True)
selected_day_en = [k for k, v in day_mapping.items() if v == selected_day_jp][0]

# 教室リスト（重複除去）
rooms = df["Room"].unique()
selected_room = st.selectbox("教室を選んでください", rooms)

# 条件で絞り込み
filtered = df[(df["Day"] == selected_day_en) & (df["Room"] == selected_room)]

if not filtered.empty:
    # 表示用に列名を日本語に変更し、時限でソート
    display_df = filtered[["Room", "Class name", "Teacher", "Period"]].copy()
    display_df.columns = ["教室", "授業名", "担当教員", "時限"]
    display_df = display_df.sort_values("時限")
    st.table(display_df)
else:
    st.info(f"{selected_day_jp}曜日の{selected_room}の授業は登録されていません。")
