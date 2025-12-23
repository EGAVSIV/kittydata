import streamlit as st
import pandas as pd
import os
import hashlib

# ================= CONFIG =================
st.set_page_config(
    page_title="🏦 समिति किट्टी सिस्टम",
    page_icon="💰",
    layout="wide"
)

EDIT_PASSWORD_HASH = hashlib.sha256("kitti123".encode()).hexdigest()

DATA_MAIN = "kitti_main.csv"
DATA_SUMMARY = "kitti_summary.csv"

MONTHS = [
    "Dec-25","Jan-26","Feb-26","Mar-26","Apr-26","May-26",
    "Jun-26","Jul-26","Aug-26","Sep-26","Oct-26","Nov-26"
]

DOUBLE_NAMES = ["श्रीमती राजबाला", "श्रीमती किरण"]

# ================= INITIAL DATA =================
def main_initial():
    return pd.DataFrame([
        [1,"A-412","श्रीमती राजेश यादव",2000],
        [2,"A-509","श्रीमती मंजू",2000],
        [3,"A-101","श्रीमती अंजू",2000],
        [4,"A-202","श्रीमती राजू",2000],
        [5,"A-810","श्रीमती सरिता",2000],
        [6,"B-407","श्रीमती प्रज्ञा",2000],
        [7,"B-203","श्रीमती मीनाक्षी",2000],
        [8,"B-201","श्रीमती संतोष",2000],
        [9,"A-307","श्रीमती राजबाला",4000],
        [10,"B-403","श्रीमती किरण",4000],
    ], columns=["SR","Flat No","Name","Kitti Amount"]
    ).assign(**{m:"" for m in MONTHS})

def summary_initial(names):
    rows = []
    for n in names:
        rows.append([n, MONTHS[0], 0])
    return pd.DataFrame(rows, columns=["Name","Month","Amount"])

# ================= LOAD / SAVE =================
def load_main():
    if not os.path.exists(DATA_MAIN):
        main_initial().to_csv(DATA_MAIN,index=False)
    return pd.read_csv(DATA_MAIN)

def load_summary(names):
    if not os.path.exists(DATA_SUMMARY):
        summary_initial(names).to_csv(DATA_SUMMARY,index=False)
    return pd.read_csv(DATA_SUMMARY)

def save_main(df): df.to_csv(DATA_MAIN,index=False)
def save_summary(df): df.to_csv(DATA_SUMMARY,index=False)

def check_pwd(p): 
    return hashlib.sha256(p.encode()).hexdigest() == EDIT_PASSWORD_HASH

# ================= UI =================
st.markdown("## 🏦 **समिति मासिक किट्टी योगदान रजिस्टर**")
st.caption("पारदर्शिता • विश्वास • सरल प्रबंधन")

main_df = load_main()

# -------- MAIN TABLE --------
st.markdown("### 📋 **मुख्य योगदान तालिका**")
st.dataframe(main_df, use_container_width=True)

st.divider()

# -------- PASSWORD --------
pwd = st.text_input("🔐 संपादन पासवर्ड", type="password")

editable = pwd and check_pwd(pwd)

# -------- EDIT MAIN TABLE --------
st.markdown("### ✏️ **मासिक एंट्री (संपादन हेतु पासवर्ड आवश्यक)**")

edited_main = st.data_editor(
    main_df,
    disabled=["SR","Flat No","Name","Kitti Amount"],
    use_container_width=True
)

if editable and st.button("💾 मुख्य तालिका सेव करें"):
    save_main(edited_main)
    st.success("डेटा सफलतापूर्वक सेव हो गया")
    st.rerun()

# -------- SUMMARY TABLE --------
st.divider()
st.markdown("### 📊 **मासिक संग्रह सारांश (Settlement Sheet)**")

names = list(edited_main["Name"]) + DOUBLE_NAMES
summary_df = load_summary(names)

summary_edit = st.data_editor(
    summary_df,
    column_config={
        "Month": st.column_config.SelectboxColumn("Month", options=MONTHS),
        "Amount": st.column_config.NumberColumn("Amount", disabled=True)
    },
    disabled=not editable,
    use_container_width=True
)

# Auto-calc amount
for i,r in summary_edit.iterrows():
    summary_edit.loc[i,"Amount"] = (
        pd.to_numeric(edited_main[r["Month"]],errors="coerce").fillna(0).sum()
    )

if editable and st.button("💾 सारांश सेव करें"):
    save_summary(summary_edit)
    st.success("सारांश अपडेट हो गया")
    st.rerun()

# ================= FOOTER =================
st.markdown("""
---
**डिज़ाइन एवं विकास**  
**Gaurav Singh Yadav**  
🩷💛🩵💙🩶💜🤍🤎💖  
समिति • पारदर्शिता • विश्वास  
""")
