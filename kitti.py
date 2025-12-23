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

FIXED_KITTI = {
    "श्रीमती राजेश यादव": 2000,
    "श्रीमती मंजू": 2000,
    "श्रीमती अंजू": 2000,
    "श्रीमती राजू": 2000,
    "श्रीमती सरिता": 2000,
    "श्रीमती प्रज्ञा": 2000,
    "श्रीमती मीनाक्षी": 2000,
    "श्रीमती संतोष": 2000,
    "श्रीमती राजबाला": 4000,
    "श्रीमती किरण": 4000,
}

DOUBLE_NAMES = ["श्रीमती राजबाला", "श्रीमती किरण"]

# ================= INITIAL DATA =================
def create_main():
    rows = []
    sr = 1
    flats = [
        ("A-412","श्रीमती राजेश यादव"),
        ("A-509","श्रीमती मंजू"),
        ("A-101","श्रीमती अंजू"),
        ("A-202","श्रीमती राजू"),
        ("A-810","श्रीमती सरिता"),
        ("B-407","श्रीमती प्रज्ञा"),
        ("B-203","श्रीमती मीनाक्षी"),
        ("B-201","श्रीमती संतोष"),
        ("A-307","श्रीमती राजबाला"),
        ("B-403","श्रीमती किरण"),
    ]
    for f,n in flats:
        row = [sr, f, n, FIXED_KITTI[n]]
        row += [""] * len(MONTHS)
        rows.append(row)
        sr += 1

    return pd.DataFrame(
        rows,
        columns=["SR","Flat No","Name","Kitti Amount"] + MONTHS
    )

def load_main():
    if not os.path.exists(DATA_MAIN):
        create_main().to_csv(DATA_MAIN,index=False)

    df = pd.read_csv(DATA_MAIN)

    # 🔒 FORCE FIXED AMOUNTS EVERY TIME
    for i,r in df.iterrows():
        df.loc[i,"Kitti Amount"] = FIXED_KITTI[r["Name"]]

    return df

def save_main(df):
    # 🔒 Reapply fixed amounts before saving
    for i,r in df.iterrows():
        df.loc[i,"Kitti Amount"] = FIXED_KITTI[r["Name"]]
    df.to_csv(DATA_MAIN,index=False)

def load_summary(names):
    if not os.path.exists(DATA_SUMMARY):
        df = pd.DataFrame(
            [[n,"",0] for n in names],
            columns=["Name","Month","Amount"]
        )
        df.to_csv(DATA_SUMMARY,index=False)
    return pd.read_csv(DATA_SUMMARY)

def save_summary(df):
    df.to_csv(DATA_SUMMARY,index=False)

def check_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest() == EDIT_PASSWORD_HASH

# ================= UI =================
st.markdown("## 🏦 **समिति किट्टी योगदान प्रणाली**")
st.caption("विश्वास • पारदर्शिता • अनुशासन")

main_df = load_main()

# -------- VIEW ONLY MAIN TABLE --------
st.markdown("### 📋 **मुख्य योगदान तालिका (View Only)**")
st.dataframe(main_df, use_container_width=True)

st.divider()

# -------- PASSWORD --------
pwd = st.text_input("🔐 संपादन हेतु पासवर्ड", type="password")
editable = pwd and check_pwd(pwd)

# -------- EDIT TABLE ONLY AFTER PASSWORD --------
if editable:
    st.success("संपादन मोड सक्रिय")

    st.markdown("### ✏️ **मासिक एंट्री (Editable)**")

    edited_main = st.data_editor(
        main_df,
        disabled=["SR","Flat No","Name","Kitti Amount"],
        use_container_width=True
    )

    if st.button("💾 मुख्य तालिका सेव करें"):
        save_main(edited_main)
        st.success("मुख्य तालिका अपडेट हो गई")
        st.rerun()

# -------- SUMMARY TABLE ALWAYS VISIBLE --------
st.divider()
st.markdown("### 📊 **मासिक संग्रह सारांश (Settlement Sheet)**")

names = list(main_df["Name"]) + DOUBLE_NAMES
summary_df = load_summary(names)

summary_edit = st.data_editor(
    summary_df,
    column_config={
        "Month": st.column_config.SelectboxColumn(
            "Month",
            options=[""] + MONTHS
        ),
        "Amount": st.column_config.NumberColumn("Amount", disabled=True)
    },
    disabled=not editable,
    use_container_width=True
)

# -------- AUTO CALC ONLY IF MONTH SELECTED --------
for i,r in summary_edit.iterrows():
    if r["Month"]:
        summary_edit.loc[i,"Amount"] = (
            pd.to_numeric(main_df[r["Month"]], errors="coerce")
            .fillna(0).sum()
        )
    else:
        summary_edit.loc[i,"Amount"] = 0

if editable and st.button("💾 सारांश सेव करें"):
    save_summary(summary_edit)
    st.success("सारांश सेव हो गया")
    st.rerun()

# ================= FOOTER =================
st.markdown("""
---
**Designed & Maintained by**  
**Gaurav Singh Yadav**  
🩷💛🩵💙🩶💜🤍🤎💖  
समिति लेखा प्रणाली  
""")
