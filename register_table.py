import streamlit as st 
import pandas as pd 
import os

st.title("新規テーブル登録ページ")

# ✅ 起動した場所にファイルを置く
csv_path = os.path.join(os.getcwd(), "course_status.csv")


if not os.path.exists(csv_path):
    df = pd.DataFrame(columns=["table","course","current_step"])
    df.to_csv(csv_path,index=False)

new_table = st.text_input("テーブル名を入力(ex:table4)")

course_options = ["スタンダードコース","プレミアムコース"]
selected_course = st.selectbox("コースを選択",course_options)

if st.button("登録する"):
    df = pd.read_csv(csv_path)

    if new_table in df["table"].values:
        st.warning("このテーブルはすでに登録されています")

    elif new_table.strip() == "":
        st.error("テーブル名を入力してください")
    
    else:
        new_row = pd.DataFrame([[new_table,selected_course,"未開始"]],columns = df.columns)
        df = pd.concat([df,new_row],ignore_index=True)
        df.to_csv(csv_path,index=False)
        st.success(f"{new_table} を {selected_course} として登録しました！")