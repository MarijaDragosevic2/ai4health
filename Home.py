import streamlit as st
import time
from common import get_base64_image, show_navbar, check_login_token, logout

# Always check login token first
login_status = check_login_token()

img_logo = get_base64_image("logo.jpeg")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "doctor" not in st.session_state:
    st.session_state["doctor"] = ""

# Page config
if st.session_state.get("logged_in", False):
    st.set_page_config(page_title="Home", layout="wide", page_icon=img_logo)
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
else:
    st.set_page_config(page_title="MammoAssist", page_icon=img_logo)

# Logout handler
def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.query_params = {}
    st.rerun()

# --------------------
# 🚪 Not logged in
# --------------------
if not st.session_state["logged_in"]:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        footer, #MainMenu {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    st.title("Welcome to MammoAssist")
    st.markdown("**Demo Login Credentials:**")
    st.markdown("- **Username:** `doctor`")
    st.markdown("- **Password:** `p`")
    st.markdown("Please log in to access the app.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            if username == "doctor" and password == "p":
                # Set session state
                st.session_state["logged_in"] = True
                st.session_state["doctor"] = "Dr. Jane Doe"
                
                # Set query params to persist login
                st.query_params["token"] = "doctor"
                
                st.success("Login successful!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid credentials.")

    # Logo and branding
    st.markdown(f"""
    <div style='text-align: center;'>
        <div style='display: flex; justify-content: center; align-items: center; gap: 10px;'>
            <img src="{img_logo}" width="100" style="border-radius: 50%;" />
            <div>
                <h4 style="margin: 0;">Code to Heal</h4>
                <h6 style="margin-top: 0.5rem;">Marija & Lucija Dragošević</h6>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------
# ✅ Logged in
# --------------------
else:
    show_navbar()

    st.title("MammoAssist")
    st.subheader(f"{st.session_state['doctor']},")

    st.markdown("""
Welcome to **MammoAssist**, your AI-assisted radiology platform for reviewing and managing mammograms efficiently.

---

### 🔍 App Overview

**MammoAssist** is designed to simulate a full clinical workflow with these capabilities:

- **MammoAI**  
  Our simulated AI assistant analyzes mammograms, identifies lesion types, assigns BI-RADS scores, and offers diagnosis recommendations.  
  Also includes doctor's notes and report saving.

- **Patients Directory**  
  View and search a database of patients. Inspect their records, medical history, and associated mammographic images.

- **Upload & View Mammograms** *(Demo Mode)*  
  Uploading is disabled in demo, but the system is prepared for importing mammograms from local devices, USBs, or CDs.



---

### What to try first?

Click the button below to explore the **AI-powered mammography workflow**:

""")

    st.page_link("pages/MammoAI.py", label="➡️ Go to MammoAI Assistant")