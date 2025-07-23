import streamlit as st
import pandas as pd

st.set_page_config(page_title="授業検索", layout="wide")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

st.title("🔍 授業名・担当教員で検索")

# 検索窓
query = st.text_input("授業名または担当教員名を入力してください")

if query:
    # 授業名または担当教員にqueryを含む行を抽出（部分一致、大文字小文字無視）
    filtered = df[
        df["Class name"].str.contains(query, case=False, na=False) |
        df["Teacher"].str.contains(query, case=False, na=False)
    ]

    if not filtered.empty:
        display_df = filtered[["Class name", "Teacher", "Room", "Day", "Period"]].copy()
        display_df.columns = ["授業名", "担当教員", "教室", "曜日", "時限"]
        st.success(f"{len(display_df)} 件の授業が見つかりました")
        st.table(display_df.sort_values(["曜日", "時限"]))
    else:
        st.warning("該当する授業が見つかりませんでした")
else:
    st.info("🔎 上の検索窓にキーワードを入力してください")
