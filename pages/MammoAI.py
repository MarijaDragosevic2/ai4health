import streamlit as st
import time
import json
import os
from datetime import date
from common import get_base64_image, show_navbar, check_login_token, ensure_login_token, logout

# Ensure login check is done first and early
login_status = check_login_token()

# If not logged in, immediately redirect to home
if not st.session_state.get("logged_in"):
    logout()

# Ensure login token is in URL
ensure_login_token()

img_logo = get_base64_image("logo.jpeg")
st.set_page_config(page_title="MammoAI", layout="wide",  page_icon=img_logo)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    margin-left: 0;
    margin-right: 0;
    padding: 0;
    max-width: 100%;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# Display common navbar (logo and doctor profile)
show_navbar()

st.title("MammoAI Assistant")

# Rest of the code remains the same as in the previous implementation
# ... (paste the rest of the original MammoAI.py code here)
# ----------------------------
# DEMO Search Disabled
# ----------------------------
with st.container():
    st.markdown("### Search Patient")
    st.info("Patient lookup is preloaded for demonstration purposes only. In the full version, you will be able to search patients in the database and run AI-powered screening on their mammograms.")

    with st.form("patient_search_form"):
        st.text_input("Patient ID", value="P001", key="patient_id_input", disabled=True)
        st.form_submit_button("Search Patient", disabled=True)

# ----------------------------
# Demo Mammogram Image Display
# ----------------------------
st.markdown("### Demo: AI Diagnosis from Radiologist Image Database")

# ----------------------------
# Patient Summary Display
# ----------------------------
patient_info = {
    "Name": "Alice Smith",
    "Patient ID": "P001",
    "Age": 48,
    "Scan Date": date.today().strftime("%Y-%m-%d"),
    "Radiologist": st.session_state.get("doctor", "Unknown")
}

st.markdown("### 📟 Patient Information")
st.markdown("""
<style>
.custom-table {
    font-size: 1.1rem;
    width: 50%;
    border-collapse: collapse;
}
.custom-table td {
    padding: 8px 12px;
    border-bottom: 1px solid #ddd;
}
.custom-table td:first-child {
    font-weight: bold;
    color: #333;
    width: 150px;
}
</style>
""", unsafe_allow_html=True)

# Render HTML table
html_table = "<table class='custom-table'>"
for key, value in patient_info.items():
    html_table += f"<tr><td>{key}</td><td>{value}</td></tr>"
html_table += "</table>"
st.markdown(html_table, unsafe_allow_html=True)

st.markdown("#### Medical History")
st.write("Family history of breast cancer. No prior biopsy. Regular screenings.")

st.markdown("#### Patient Record")
st.write("2023-05-01: Regular screening shows benign findings. Follow-up in 1 year.")
# ----------------------------
# Radiologist Images
# ----------------------------
with st.container():
    st.info("The images are fetched from a sample radiologist database.")
    cols = st.columns(4)
    image_paths = ["Image-1.jpg", "Image-3.jpg", "Image-0.jpg", "Image-2.jpg"]
    for i, col in enumerate(cols):
        with col:
            st.image(image_paths[i], caption=f"View {i+1}", use_container_width=True)

# Trigger AI simulation
if st.button("Show AI Diagnosis"):
    st.success("AI detection displayed.")
    st.session_state["diagnosis"] = ("Malignant", 94)
    st.session_state["show_ai"] = True
    st.session_state["annotated_images"] = ["anot1.JPG", "anot2.JPG"]

# ----------------------------
# AI Output (if triggered)
# ----------------------------
if st.session_state.get("show_ai") and "diagnosis" in st.session_state:
    st.markdown("### AI Annotated Images")
    cols_annotated = st.columns(2)
    for i, col in enumerate(cols_annotated):
        with col:
            st.image(st.session_state["annotated_images"][i], caption=f"AI Annotated {i+1}", use_container_width=True)

    diag, conf = st.session_state["diagnosis"]
    birads = "BI-RADS 5"
    lesion_type = "Calcification"

    st.markdown("### AI Evaluation")
    st.markdown(f"**BI-RADS Score:** {birads}")
    st.markdown(f"**Lesion Type:** {lesion_type}")
    if diag == "Malignant":
        st.error(f"⚠️ **{diag}** (Confidence: {conf}%)")
    else:
        st.success(f"✅ **{diag}** (Confidence: {conf}%)")

    rec = "🔴 Biopsy recommended." if diag == "Malignant" else "🟢 Regular follow-up recommended."
    st.markdown(f"**Recommendation:** {rec}")

    # ----------------------------
    # Doctor's Report Input (Hardcoded for Demo)
    # ----------------------------
    st.markdown("### Doctor's Report")
    notes = st.text_area(
        "Write your interpretation or comments below:",
        value=st.session_state.get("doctor_notes", ""),
        placeholder="Example: Lesion appears suspicious. Recommend biopsy and MRI follow-up.",
        height=150
    )

    if st.button("📂 Save Report to Patient Record"):
        st.session_state["doctor_notes"] = notes
        st.success("✅ Report saved.")
