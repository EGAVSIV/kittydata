import streamlit as st
import pandas as pd
import os
import hashlib

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Society Kitti System", layout="wide")

DATA_FILE = "kitti_data.csv"
EDIT_PASSWORD_HASH = hashlib.sha256("kitti123".encode()).hexdigest()

MONTHS = [
    "Dec-25", "Jan-26", "Feb-26", "Mar-26", "Apr-26", "May-26",
    "Jun-26", "Jul-26", "Aug-26", "Sep-26", "Oct-26", "Nov-26"
]

# ================================
# INITIAL DATA
# ================================
def initial_data():
    return pd.DataFrame([
        ["A-412", "Smt Rajesh Yadav", 2000] + [""]*12 + ["Smt Rajesh Yadav", 14000],
        ["A-509", "Smt Manju", 2000] + [""]*12 + ["", ""],
        ["A-101", "Smt Anju", ""] + [""]*12 + ["", ""],
        ["A-202", "Smt Raju", ""] + [""]*12 + ["", ""],
        ["A-810", "Smt Sarita", ""] + [""]*12 + ["", ""],
        ["B-407", "Smt Pragya", 2000] + [""]*12 + ["", ""],
        ["B-203", "Smt Minakshi", 2000] + [""]*12 + ["", ""],
        ["B-201", "Smt Santosh", 2000] + [""]*12 + ["", ""],
        ["A-307", "Smt Rajbala", ""] + [""]*12 + ["", ""],
        ["B-403", "Smt Kiran", 4000] + [""]*12 + ["", ""],
    ], columns=[
        "Flat No", "Name", "Kitti Amount"
    ] + MONTHS + ["Kitti Utai", "Amount"])

# ================================
# LOAD / SAVE
# ================================
def load_data():
    if not os.path.exists(DATA_FILE):
        df = initial_data()
        df.to_csv(DATA_FILE, index=False)
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ================================
# PASSWORD CHECK
# ================================
def check_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest() == EDIT_PASSWORD_HASH

# ================================
# UI
# ================================
st.title("🏦 Society Kitti Contribution System")

df = load_data()

# ---- VIEW MODE ----
st.subheader("📋 View Kitti Records")
st.dataframe(df, use_container_width=True)

st.divider()

# ---- EDIT SECTION ----
st.subheader("✏️ Edit Mode (Password Required)")

pwd = st.text_input("Enter Edit Password", type="password")

if pwd:
    if check_password(pwd):
        st.success("Edit Access Granted")

        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True
        )

        # ---- AUTO TOTAL ROW ----
        try:
            total_row = ["Total", "", edited_df["Kitti Amount"].fillna(0).astype(float).sum()]
            for m in MONTHS:
                total_row.append("")
            total_row += ["", edited_df["Amount"].fillna(0).astype(float).sum()]

            edited_df = edited_df[edited_df["Flat No"] != "Total"]
            edited_df.loc[len(edited_df)] = total_row
        except:
            pass

        if st.button("💾 Save Changes"):
            save_data(edited_df)
            st.success("Data Saved Successfully")
            st.rerun()
    else:
        st.error("Incorrect Password")

# ================================
# FOOTER
# ================================
st.markdown("""
---
**Designed by – Gaurav Singh Yadav**  
🩷💛🩵💙🩶💜🤍🤎💖  
Society | Community | Trust System  
""")
