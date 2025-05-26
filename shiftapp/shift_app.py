import streamlit as st
import csv
import os
import pandas as pd

st.title("シフト管理アプリ")

page = st.sidebar.selectbox(
    "ページを選択してください",
    ["シフト承認（管理者）", "確定シフト一覧"]
)

if page == "シフト承認（管理者）":
    st.subheader("申請一覧（管理者用）")
    try:
        df = pd.read_csv("shift_requests.csv", header=None, names=["日付", "開始", "終了", "メモ"])
        st.dataframe(df)

        for i, row in df.iterrows():
            name = row["メモ"] if row["メモ"] else "未登録"
            st.write(f"{row['日付']} | {row['開始']}〜{row['終了']} | 名前: {name}")

            if f"approved_{i}" not in st.session_state:
                st.session_state[f"approved_{i}"] = False

            if st.button(f"承認_{i}"):
                st.session_state[f"approved_{i}"] = True
                st.success(f"{row['日付']} を承認しました！")

        if st.button("変更を保存", key="save_changes"):
            with open("confirmed_shifts.csv", "a", newline="") as f:
                writer = csv.writer(f)

                # ヘッダーチェック
                need_header = True
                if os.path.exists("confirmed_shifts.csv"):
                    with open("confirmed_shifts.csv", newline="") as checkfile:
                        if sum(1 for _ in checkfile) > 0:
                            need_header = False

                if need_header:
                    writer.writerow(["日付", "開始", "終了", "名前"])

                keep_rows = []
                for i, row in df.iterrows():
                    if st.session_state.get(f"approved_{i}", False):
                        name = row["メモ"] if row["メモ"] else "未登録"
                        writer.writerow([row["日付"], row["開始"], row["終了"], name])
                    else:
                        keep_rows.append(row)

            # 残すデータのみ再保存
            if keep_rows:
                pd.DataFrame(keep_rows).to_csv("shift_requests.csv", index=False, header=False)
            else:
                open("shift_requests.csv", "w").close()

            st.success("承認済みの申請を保存しました！")

    except FileNotFoundError:
        st.info("申請データがありません。")

elif page == "確定シフト一覧":
    st.subheader("確定シフト一覧")
    try:
        confirmed_df = pd.read_csv("confirmed_shifts.csv")
        st.dataframe(confirmed_df)
    except FileNotFoundError:
        st.info("まだ確定シフトがありません。")






        



