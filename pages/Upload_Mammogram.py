import streamlit as st
import time
import json
import os
from common import get_base64_image, show_navbar, check_login_token, ensure_login_token, logout

# Ensure login check is done first and early
login_status = check_login_token()

# If not logged in, immediately redirect to home
if not st.session_state.get("logged_in"):
    logout()
    
# Ensure login token is in URL
ensure_login_token()

img_logo = get_base64_image("logo.jpeg")
st.set_page_config(page_title="Upload Mammogram", page_icon="", layout="wide")

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

# Load patients function
def load_patients():
    with open("patients.json", "r") as f:
        return json.load(f)

def save_patients(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=2)

st.title("Upload & View Image")

# ----------------------------
# Disabled Uploader (Demo Mode Only)
# ----------------------------
st.markdown("""
<div style="color:gray; ">
    This feature is disabled in demo mode. <br>
    In the full version, you will be able to upload and analyze mammograms directly from your local machine. <br>
    This includes images brought by patients from other institutions — for example, stored on a CD, USB drive, or other external media — 
    even if those patients are not yet in the hospital database.
</div>
""", unsafe_allow_html=True)
st.file_uploader("Upload Disabled", disabled=True)

# ----------------------------
# Automatic Save of Patient Record
# ----------------------------
if ("current_patient" in st.session_state and 
    not st.session_state.get("record_saved", False)):

    current = st.session_state["current_patient"]

    # Simulate storing the image as a reference
    demo_image_name = f"UploadedImage_{current['id']}_{int(time.time())}"
    if "images" not in current:
        current["images"] = []
    current["images"].append(demo_image_name)

    # Update or append to patients.json
    patients_data = load_patients()
    exists = False
    for i, p in enumerate(patients_data):
        if p["id"].strip().upper() == current["id"].strip().upper():
            patients_data[i] = current
            exists = True
            break
    if not exists:
        patients_data.append(current)

    save_patients(patients_data)
    st.cache_data.clear()
    st.session_state["record_saved"] = True
    st.success("Patient record automatically saved!")

# ----------------------------
# Next Step Navigation
# ----------------------------
st.markdown("----")

if st.button("➡️ Proceed to MammoAI"):
    st.switch_page("pages/MammoAI.py")  # Adjust path if necessary