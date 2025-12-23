import streamlit as st
import pandas as pd
import os
import hashlib

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Manglam Anchal Kitti – Sundarkand",
    page_icon="💰",
    layout="wide"
)

# ================= HEADER =================
st.markdown(
    """
    <div style="text-align:center; font-size:30px; font-weight:700;">
        🙏 श्री हनुमते नमः 🙏
    </div>
    <div style="text-align:center; font-size:20px; margin-top:5px;">
        Manglam Anchal Kitti <b>"Sundarkand"</b>
    </div>
    <div style="text-align:center; color:gray; margin-top:5px;">
        View only — Enter password to edit
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)

# ================= CONSTANTS =================
EDIT_PASSWORD_HASH = hashlib.sha256("kitti123".encode()).hexdigest()
MAIN_FILE = "kitti_main.csv"
SUMMARY_FILE = "kitti_monthly_summary.csv"

MONTHS = [
    "Dec-25","Jan-26","Feb-26","Mar-26","Apr-26","May-26",
    "Jun-26","Jul-26","Aug-26","Sep-26","Oct-26","Nov-26"
]

FIXED_KITTI_BY_SR = {
    1:2000,2:2000,3:2000,4:2000,5:2000,
    6:2000,7:2000,8:2000,9:4000,10:4000
}

MASTER = [
    (1,"A-412","श्रीमती राजेश यादव"),
    (2,"A-509","श्रीमती मंजू"),
    (3,"A-101","श्रीमती अंजू"),
    (4,"A-202","श्रीमती राजू"),
    (5,"A-810","श्रीमती सरिता"),
    (6,"B-407","श्रीमती प्रज्ञा"),
    (7,"B-203","श्रीमती मीनाक्षी"),
    (8,"B-201","श्रीमती संतोष"),
    (9,"A-307","श्रीमती राजबाला"),
    (10,"B-403","श्रीमती किरण"),
]

# ================= DATA FUNCTIONS =================
def create_main():
    rows = []
    for sr, flat, name in MASTER:
        row = {
            "SR": sr,
            "Flat No": flat,
            "Name": name,
            "Kitti Amount": FIXED_KITTI_BY_SR[sr],
        }
        for m in MONTHS:
            row[m] = ""
        rows.append(row)
    return pd.DataFrame(rows)

def load_main():
    if not os.path.exists(MAIN_FILE):
        create_main().to_csv(MAIN_FILE, index=False)

    df = pd.read_csv(MAIN_FILE)
    for i, r in df.iterrows():
        df.loc[i, "Kitti Amount"] = FIXED_KITTI_BY_SR[int(r["SR"])]
    return df

def save_main(df):
    for i, r in df.iterrows():
        df.loc[i, "Kitti Amount"] = FIXED_KITTI_BY_SR[int(r["SR"])]
    df.to_csv(MAIN_FILE, index=False)

def load_summary():
    if not os.path.exists(SUMMARY_FILE):
        df = pd.DataFrame({
            "Month": MONTHS,
            "Name": ["None"] * len(MONTHS)
        })
        df.to_csv(SUMMARY_FILE, index=False)

    return pd.read_csv(SUMMARY_FILE)

def save_summary(df):
    df[["Month", "Name"]].to_csv(SUMMARY_FILE, index=False)

def check_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest() == EDIT_PASSWORD_HASH

# ================= LOAD DATA =================
main_df = load_main()
summary_saved = load_summary()

# ================= FORM =================
with st.form("kitti_form"):

    pwd = st.text_input("🔐 Edit Password", type="password")
    can_edit = pwd and check_pwd(pwd)

    # ---------- MAIN TABLE ----------
    st.markdown("### 📋 मुख्य योगदान तालिका")

    edited_main = st.data_editor(
        main_df,
        disabled=(["SR","Flat No","Name","Kitti Amount"] if can_edit else list(main_df.columns)),
        use_container_width=True
    )

    # ---------- MONTHLY TOTAL TABLE ----------
    st.markdown("### 📊 मासिक कुल संग्रह")

    summary_rows = []

    for m in MONTHS:
        total_amount = pd.to_numeric(
            edited_main[m], errors="coerce"
        ).fillna(0).sum()

        saved_name = summary_saved.loc[
            summary_saved["Month"] == m, "Name"
        ].values[0]

        summary_rows.append({
            "Name": saved_name,
            "Month": m,
            "Amount": total_amount
        })

    summary_df = pd.DataFrame(summary_rows)

    edited_summary = st.data_editor(
        summary_df,
        column_config={
            "Name": st.column_config.SelectboxColumn(
                "Name",
                options=["None"] + list(main_df["Name"].unique()),
                required=False
            ),
            "Month": st.column_config.TextColumn("Month", disabled=True),
            "Amount": st.column_config.NumberColumn("Amount", disabled=True)
        },
        hide_index=True,
        use_container_width=True
    )

    # ---------- SAVE ----------
    submitted = st.form_submit_button("💾 Save Changes")

    if submitted:
        if not can_edit:
            st.error("Incorrect password — cannot save")
        else:
            save_main(edited_main)
            save_summary(edited_summary)
            st.success("डेटा सफलतापूर्वक सेव हो गया")

# ================= FOOTER =================
st.markdown("""
---
**Designed & Maintained by**  
**Gaurav Singh Yadav**
""")
