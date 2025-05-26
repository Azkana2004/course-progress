import streamlit as st
import pandas as pd
import os

st.title("コース料理進行状況")
csv_path = "course_status.csv"

if not os.path.exists(csv_path):
    st.warning("進行状況ファイルがまだ存在しません。先に登録してください。")
    st.stop()

df = pd.read_csv(csv_path)

if df.empty:
    st.info("まだテーブルが登録されていません。")
    st.stop()

for _,row in df.iterrows():
    st.subheader(f"{row['table']} ({row['course']})")
    st.write(f"現在のステータス：**{row['current_step']}**")