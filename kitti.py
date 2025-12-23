import streamlit as st
import pandas as pd
import os
import hashlib

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Society Kitti System", layout="wide")

DATA_FILE = "kitti_main.csv"
SUMMARY_FILE = "kitti_summary.csv"

EDIT_PASSWORD_HASH = hashlib.sha256("kitti123".encode()).hexdigest()

MONTHS = [
    "Dec-25", "Jan-26", "Feb-26", "Mar-26", "Apr-26", "May-26",
    "Jun-26", "Jul-26", "Aug-26", "Sep-26", "Oct-26", "Nov-26"
]

DOUBLE_CONTRIBUTORS = ["Smt Rajesh Yadav", "Smt Kiran"]

# ================================
# INITIAL DATA
# ================================
def initial_main_data():
    return pd.DataFrame([
        ["A-412", "Smt Rajesh Yadav", 2000] + [""]*12,
        ["A-509", "Smt Manju", 2000] + [""]*12,
        ["A-101", "Smt Anju", 2000] + [""]*12,
        ["A-202", "Smt Raju", 2000] + [""]*12,
        ["A-810", "Smt Sarita", 2000] + [""]*12,
        ["B-407", "Smt Pragya", 2000] + [""]*12,
        ["B-203", "Smt Minakshi", 2000] + [""]*12,
        ["B-201", "Smt Santosh", 2000] + [""]*12,
        ["A-307", "Smt Rajbala", 4000] + [""]*12,
        ["B-403", "Smt Kiran", 4000] + [""]*12,
    ], columns=["Flat No", "Name", "Kitti Amount"] + MONTHS)

def initial_summary_data(names):
    rows = []
    for n in names:
        rows.append([n, MONTHS[0], 0])
    return pd.DataFrame(rows, columns=["Name", "Month", "Amount"])

# ================================
# LOAD / SAVE
# ================================
def load_main():
    if not os.path.exists(DATA_FILE):
        df = initial_main_data()
        df.to_csv(DATA_FILE, index=False)
    return pd.read_csv(DATA_FILE)

def load_summary(names):
    if not os.path.exists(SUMMARY_FILE):
        df = initial_summary_data(names)
        df.to_csv(SUMMARY_FILE, index=False)
    return pd.read_csv(SUMMARY_FILE)

def save_main(df):
    df.to_csv(DATA_FILE, index=False)

def save_summary(df):
    df.to_csv(SUMMARY_FILE, index=False)

# ================================
# PASSWORD CHECK
# ================================
def check_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest() == EDIT_PASSWORD_HASH

# ================================
# CALCULATE MONTH TOTAL
# ================================
def calculate_month_total(df, month):
    return pd.to_numeric(df[month], errors="coerce").fillna(0).sum()

# ================================
# UI
# ================================
st.title("🏦 Society Kitti Contribution System")

main_df = load_main()

# -------- VIEW MAIN TABLE --------
st.subheader("📋 Monthly Contribution Register")
st.dataframe(main_df, use_container_width=True)

st.divider()

pwd = st.text_input("🔐 Enter Edit Password", type="password")

if pwd and check_password(pwd):
    st.success("Edit Access Enabled")

    # -------- EDIT MAIN TABLE --------
    edited_main = st.data_editor(
        main_df,
        use_container_width=True,
        num_rows="dynamic"
    )

    if st.button("💾 Save Main Table"):
        save_main(edited_main)
        st.success("Main Table Updated")
        st.rerun()

    # -------- SUMMARY TABLE --------
    st.divider()
    st.subheader("📊 Monthly Collection Summary")

    names = list(edited_main["Name"])
    for d in DOUBLE_CONTRIBUTORS:
        names.append(d)

    summary_df = load_summary(names)

    # Dropdown for month
    summary_df["Month"] = summary_df["Month"].astype(str)

    edited_summary = st.data_editor(
        summary_df,
        column_config={
            "Month": st.column_config.SelectboxColumn(
                "Month",
                options=MONTHS
            ),
            "Amount": st.column_config.NumberColumn(
                "Amount",
                disabled=True
            )
        },
        use_container_width=True
    )

    # Auto-update Amount column
    for i, r in edited_summary.iterrows():
        edited_summary.loc[i, "Amount"] = calculate_month_total(
            edited_main, r["Month"]
        )

    if st.button("💾 Save Summary Table"):
        save_summary(edited_summary)
        st.success("Summary Table Updated")
        st.rerun()

elif pwd:
    st.error("Incorrect Password")

# ================================
# FOOTER
# ================================
st.markdown("""
---
**Designed by – Gaurav Singh Yadav**  
🩷💛🩵💙🩶💜🤍🤎💖  
Society | Trust | Transparency  
""")
