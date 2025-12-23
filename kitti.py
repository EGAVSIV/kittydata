import streamlit as st
import pandas as pd
import os
import hashlib

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="समिति किट्टी सिस्टम",
    page_icon="💰",
    layout="wide"
)

# ==============================
# CONSTANTS
# ==============================
EDIT_PASSWORD_HASH = hashlib.sha256("kitti123".encode()).hexdigest()

MAIN_FILE = "kitti_main.csv"
SUMMARY_FILE = "kitti_summary.csv"

MONTHS = [
    "Dec-25","Jan-26","Feb-26","Mar-26","Apr-26","May-26",
    "Jun-26","Jul-26","Aug-26","Sep-26","Oct-26","Nov-26"
]

# SR BASED FIXED AMOUNT (SAFE)
FIXED_KITTI_BY_SR = {
    1: 2000,
    2: 2000,
    3: 2000,
    4: 2000,
    5: 2000,
    6: 2000,
    7: 2000,
    8: 2000,
    9: 4000,
    10: 4000,
}

DOUBLE_SR = [9, 10]

# ==============================
# CREATE MAIN TABLE
# ==============================
def create_main():
    data = [
        [1,"A-412","श्रीमती राजेश यादव"],
        [2,"A-509","श्रीमती मंजू"],
        [3,"A-101","श्रीमती अंजू"],
        [4,"A-202","श्रीमती राजू"],
        [5,"A-810","श्रीमती सरिता"],
        [6,"B-407","श्रीमती प्रज्ञा"],
        [7,"B-203","श्रीमती मीनाक्षी"],
        [8,"B-201","श्रीमती संतोष"],
        [9,"A-307","श्रीमती राजबाला"],
        [10,"B-403","श्रीमती किरण"],
    ]

    rows = []
    for sr, flat, name in data:
        row = {
            "SR": sr,
            "Flat No": flat,
            "Name": name,
            "Kitti Amount": FIXED_KITTI_BY_SR[sr]
        }
        for m in MONTHS:
            row[m] = ""
        rows.append(row)

    return pd.DataFrame(rows)

# ==============================
# LOAD / SAVE MAIN
# ==============================
def load_main():
    if not os.path.exists(MAIN_FILE):
        create_main().to_csv(MAIN_FILE, index=False)

    df = pd.read_csv(MAIN_FILE)

    # FORCE FIXED AMOUNT (ALWAYS)
    for i, r in df.iterrows():
        sr = int(r["SR"])
        df.loc[i, "Kitti Amount"] = FIXED_KITTI_BY_SR[sr]

    return df

def save_main(df):
    for i, r in df.iterrows():
        sr = int(r["SR"])
        df.loc[i, "Kitti Amount"] = FIXED_KITTI_BY_SR[sr]

    df.to_csv(MAIN_FILE, index=False)

# ==============================
# LOAD / SAVE SUMMARY
# ==============================
def load_summary(names):
    if not os.path.exists(SUMMARY_FILE):
        rows = [[n, "", 0] for n in names]
        pd.DataFrame(rows, columns=["Name","Month","Amount"]).to_csv(SUMMARY_FILE, index=False)

    return pd.read_csv(SUMMARY_FILE)

def save_summary(df):
    df.to_csv(SUMMARY_FILE, index=False)

# ==============================
# PASSWORD CHECK
# ==============================
def check_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest() == EDIT_PASSWORD_HASH

# ==============================
# UI START
# ==============================
st.markdown("## 🏦 **समिति मासिक किट्टी योगदान प्रणाली**")
st.caption("विश्वास • पारदर्शिता • अनुशासन")

# ==============================
# MAIN TABLE (VIEW ONLY)
# ==============================
main_df = load_main()

st.markdown("### 📋 मुख्य योगदान तालिका (केवल देखने हेतु)")
st.dataframe(main_df, use_container_width=True)

st.divider()

# ==============================
# PASSWORD INPUT
# ==============================
pwd = st.text_input("🔐 संपादन पासवर्ड", type="password")
editable = pwd and check_pwd(pwd)

# ==============================
# EDIT MAIN TABLE
# ==============================
if editable:
    st.success("संपादन मोड सक्रिय")

    st.markdown("### ✏️ मासिक एंट्री (Editable)")

    edited_main = st.data_editor(
        main_df,
        disabled=["SR","Flat No","Name","Kitti Amount"],
        use_container_width=True
    )

    if st.button("💾 मुख्य तालिका सेव करें"):
        save_main(edited_main)
        st.success("मुख्य तालिका अपडेट हो गई")
        st.rerun()

# ==============================
# SUMMARY TABLE (ALWAYS VISIBLE)
# ==============================
st.divider()
st.markdown("### 📊 मासिक संग्रह सारांश (Settlement Sheet)")

names = list(main_df["Name"])
for sr in DOUBLE_SR:
    names.append(main_df.loc[main_df["SR"] == sr, "Name"].values[0])

summary_df = load_summary(names)

summary_edit = st.data_editor(
    summary_df,
    column_config={
        "Month": st.column_config.SelectboxColumn(
            "Month",
            options=[""] + MONTHS
        ),
        "Amount": st.column_config.NumberColumn(
            "Amount",
            disabled=True
        )
    },
    disabled=not editable,
    use_container_width=True
)

# AUTO CALC AMOUNT
for i, r in summary_edit.iterrows():
    if r["Month"]:
        summary_edit.loc[i, "Amount"] = (
            pd.to_numeric(main_df[r["Month"]], errors="coerce")
            .fillna(0)
            .sum()
        )
    else:
        summary_edit.loc[i, "Amount"] = 0

if editable and st.button("💾 सारांश सेव करें"):
    save_summary(summary_edit)
    st.success("सारांश सेव हो गया")
    st.rerun()

# ==============================
# FOOTER
# ==============================
st.markdown("""
---
**Designed & Maintained by**  
**Gaurav Singh Yadav**  
🩷💛🩵💙🩶💜🤍🤎💖  
समिति लेखा एवं पारदर्शिता प्रणाली  
""")
