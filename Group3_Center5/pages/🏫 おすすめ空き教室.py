import streamlit as st
import pandas as pd

st.set_page_config(page_title="おすすめ空き教室", layout="wide")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

st.title("🏫 おすすめ空き教室検索")

# --- 入力UI ---
st.markdown("### 📅 曜日を選んでください")
days_jp = ["月", "火", "水", "木", "金"]
day_mapping = {
    "月": "Monday", "火": "Tuesday", "水": "Wednesday", "木": "Thursday", "金": "Friday"
}
selected_day_jp = st.radio("", days_jp, horizontal=True)
selected_day_en = day_mapping[selected_day_jp]

st.markdown("### ⏰ 時限を選んでください")
periods = sorted(df["Period"].dropna().unique())
period_options = [f"{int(p)}限" for p in periods]
period_map = {f"{int(p)}限": int(p) for p in periods}
selected_period_label = st.radio("", period_options, horizontal=True)
selected_period = period_map[selected_period_label]

# --- 教室リスト ---
floor_3_rooms = ['5301', '5302', '5303', '5304', '5305', '5306', '5307', '5308',
                 '5309', '5310', '5311', '5312', '5313']
floor_4_rooms = ['5401', '5402', '5403', '5404', '5405', '5406', '5407', '5408',
                 '5409', '5410', '5411', '5412', '5413', '5414', '5415', '5416', '5417']
all_rooms = floor_3_rooms + floor_4_rooms

# --- 授業データから使用中の教室を抽出 ---
used_rooms = df[
    (df["Day"] == selected_day_en) &
    (df["Period"] == selected_period)
]["Room"].astype(str).unique().tolist()

# --- 空いている教室を抽出 ---
available_rooms = sorted([room for room in all_rooms if room not in used_rooms])

# --- 表示 ---
if available_rooms:
    st.success(f"✅ {selected_day_jp}曜日 {selected_period_label} に空いている教室は {len(available_rooms)} 室あります")
    st.write("### 🟢 空き教室一覧")
    st.table(pd.DataFrame(available_rooms, columns=["空き教室"]))
else:
    st.warning(f"😢 {selected_day_jp}曜日 {selected_period_label} に空いている教室はありません")
