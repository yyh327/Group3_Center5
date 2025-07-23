import streamlit as st
import pandas as pd

st.set_page_config(page_title="Recommended Available Classroom", layout="wide")

# --- CSV読み込み / Load CSV ---
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

# --- タイトル / Title ---
st.markdown("""
### 🏫 おすすめ空き教室検索  
<span style='font-size: 1em; color: gray;'>(Recommended Available Classroom Search)</span>
""", unsafe_allow_html=True)

# --- 曜日選択 / Day Selection ---
st.markdown("""
### 📅 曜日を選んでください  
<span style='font-size: 1em; color: gray;'>(Please select a day)</span>
""", unsafe_allow_html=True)

days_jp = ["月", "火", "水", "木", "金"]
day_mapping = {
    "月": "Monday", "火": "Tuesday", "水": "Wednesday", "木": "Thursday", "金": "Friday"
}
selected_day_jp = st.radio("", days_jp, horizontal=True)
selected_day_en = day_mapping[selected_day_jp]

# --- 時限選択 / Period Selection ---
st.markdown("""
### ⏰ 時限を選んでください  
<span style='font-size: 1em; color: gray;'>(Please select a period)</span>
""", unsafe_allow_html=True)

periods = sorted(df["Period"].dropna().unique())
period_options = [f"{int(p)}限" for p in periods]
period_map = {f"{int(p)}限": int(p) for p in periods}
selected_period_label = st.radio("", period_options, horizontal=True)
selected_period = period_map[selected_period_label]

# --- 教室リスト / Classroom List ---
floor_3_rooms = ['5301', '5302', '5303', '5304', '5305', '5306', '5307', '5308',
                 '5309', '5310', '5311', '5312', '5313']
floor_4_rooms = ['5401', '5402', '5403', '5404', '5405', '5406', '5407', '5408',
                 '5409', '5410', '5411', '5412', '5413', '5414', '5415', '5416', '5417']
all_rooms = floor_3_rooms + floor_4_rooms

# --- 使用中教室の抽出 / Get Used Classrooms ---
used_rooms = df[
    (df["Day"] == selected_day_en) &
    (df["Period"] == selected_period)
]["Room"].astype(str).unique().tolist()

# --- 空き教室の抽出 / Get Available Classrooms ---
available_rooms = sorted([room for room in all_rooms if room not in used_rooms])

# --- 表示 / Display ---
if available_rooms:
    st.success(f"✅ {selected_day_jp}曜日 {selected_period_label} に空いている教室は {len(available_rooms)} 室あります")
    st.markdown("""
    ### 🟢 空き教室一覧  
    <span style='font-size: 1em; color: gray;'>(List of Available Classrooms)</span>
    """, unsafe_allow_html=True)
    st.table(pd.DataFrame(available_rooms, columns=["空き教室 / Available Room"]))
else:
    st.warning(f"😢 {selected_day_jp}曜日 {selected_period_label} に空いている教室はありません")
