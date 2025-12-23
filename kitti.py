import streamlit as st
import pandas as pd
import os
import hashlib

# ================= CONFIG =================
st.set_page_config(
    page_title="समिति किट्टी सिस्टम",
    page_icon="💰",
    layout="wide"
)

st.markdown(
    """
    <div style="text-align:center; font-size:28px; font-weight:700; margin-bottom:10px;">
        🙏 श्री हनुमते नमः 🙏
    </div>
    """,
    unsafe_allow_html=True
)

EDIT_PASSWORD_HASH = hashlib.sha256("kitti123".encode()).hexdigest()

MAIN_FILE = "kitti_main.csv"

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

# ================= DATA =================
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

    # Force fixed amount
    for i, r in df.iterrows():
        df.loc[i, "Kitti Amount"] = FIXED_KITTI_BY_SR[int(r["SR"])]

    return df

def save_main(df):
    for i, r in df.iterrows():
        df.loc[i, "Kitti Amount"] = FIXED_KITTI_BY_SR[int(r["SR"])]
    df.to_csv(MAIN_FILE, index=False)

def check_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest() == EDIT_PASSWORD_HASH

# ================= UI =================
st.markdown("## 🏦 **समिति मासिक किट्टी योगदान प्रणाली**")

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

main_df = load_main()

# -------- MAIN TABLE (VIEW) --------
st.markdown("### 📋 **मुख्य योगदान तालिका (केवल देखने हेतु)**")
st.dataframe(main_df, use_container_width=True)

pwd = st.text_input("🔐 संपादन पासवर्ड", type="password")

if pwd and check_pwd(pwd) and not st.session_state.edit_mode:
    if st.button("✏️ Edit Main Table"):
        st.session_state.edit_mode = True
        st.rerun()

# -------- EDIT MODE --------
if st.session_state.edit_mode:
    st.markdown("### ✏️ **मासिक एंट्री (Editable Mode)**")

    edited = st.data_editor(
        main_df,
        disabled=["SR","Flat No","Name","Kitti Amount"],
        use_container_width=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save"):
            save_main(edited)
            st.success("डेटा सेव हो गया")
            st.rerun()

    with col2:
        if st.button("✅ OK (Exit Edit Mode)"):
            st.session_state.edit_mode = False
            st.rerun()

# -------- MONTH TOTALS --------
st.divider()
st.markdown("### 📊 **मासिक कुल संग्रह (Auto Calculated)**")

month_totals = {
    m: pd.to_numeric(main_df[m], errors="coerce").fillna(0).sum()
    for m in MONTHS
}

total_df = pd.DataFrame(
    [[m, month_totals[m]] for m in MONTHS],
    columns=["Month", "Total Collection"]
)

st.dataframe(total_df, use_container_width=True)

# ================= FOOTER =================
st.markdown("""
---
**Designed & Maintained by**  
**Gaurav Singh Yadav**  
""")
