import streamlit as st
import pandas as pd

st.set_page_config(page_title="授業検索", layout="wide")

# CSV読み込み
df = pd.read_csv("/mount/src/group3_center5/Group3_Center5/pages/data.csv", encoding="shift_jis")

st.title("🔍 授業名・担当教員で検索")

# 検索窓
query = st.text_input("授業名または担当教員名を入力してください（例：田中、リテラシー）")

if query:
    # ひらがな→カタカナに変換（あいまい検索対策）
    query_kana = jaconv.hira2kata(query)

    # 授業名または担当教員にquery（または変換後文字列）を含む行を抽出
    filtered = df[
        df["Class name"].str.contains(query, case=False, na=False) |
        df["Class name"].str.contains(query_kana, na=False) |
        df["Teacher"].str.contains(query, case=False, na=False) |
        df["Teacher"].str.contains(query_kana, na=False)
    ]

    if not filtered.empty:
        # 表示用データ（検索一覧）
        preview_df = filtered[["Class name", "Teacher"]].drop_duplicates().reset_index(drop=True)
        preview_df.index += 1  # 行番号を1から開始に（見た目用）

        st.success(f"{len(preview_df)} 件の授業が見つかりました")
        selected_index = st.radio("詳細を見たい授業を選んでください", preview_df.index, format_func=lambda i: f"{preview_df.loc[i, 'Class name']}（{preview_df.loc[i, 'Teacher']}）")

        # 詳細データを抽出・表示
        selected_row = preview_df.loc[selected_index]
        detail_filtered = filtered[
            (filtered["Class name"] == selected_row["Class name"]) &
            (filtered["Teacher"] == selected_row["Teacher"])
        ]

        detail_df = detail_filtered[["Class name", "Teacher", "Room", "Day", "Period"]].copy()
        detail_df.columns = ["授業名", "担当教員", "教室", "曜日", "時限"]
        detail_df = detail_df.sort_values(["曜日", "時限"])

        st.write("### 📋 授業の詳細")
        st.table(detail_df)

    else:
        st.warning("該当する授業が見つかりませんでした")

else:
    st.info("🔎 上の検索窓にキーワードを入力してください")

