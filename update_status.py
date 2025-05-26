import streamlit as st
import pandas as pd 
import os 

st.title("ステータス更新ページ")

csv_path = "course_status.csv"

if not os.path.exists(csv_path):
    st.warning("course_status.csv が存在しません。まず登録ページからテーブルを追加してください。")
    st.stop()

df = pd.read_csv(csv_path)

course_menus = {
    "スタンダードコース": ["前菜", "スープ", "ポワソン", "グラニテ", "ビアンド", "カレー", "デセール"],
    "プレミアムコース": ["冷菜", "温菜", "スープ", "ポワソン", "グラニテ", "ビアンド", "カレー", "アヴァンデセール", "デセール"]
}

selected_table = st.selectbox("テーブルを選択",df["table"])

selected_course = df[df["table"] == selected_table]["course"].values[0]
st.write(f"選択されたコース：{selected_course}")

menu_list = course_menus[selected_course]
selected_dish = st.selectbox("料理を選択",menu_list)

# ステータスを選ぶボタン
col1, col2, col3 = st.columns(3)

def update_status(new_status):
    updated_value = f"{selected_dish} - {new_status}"
    df.loc[df["table"] == selected_table,"current_step"] = updated_value
    df.to_csv(csv_path, index=False)
    st.success(f"{selected_table} を「{updated_value}」に更新しました！")


with col1:
    if st.button("声かけ"):
        update_status("声かけ")

with col2:
    if st.button("提供"):
        update_status("提供")

with col3:
    if st.button("マジック中"):
        update_status("マジック中")
