import streamlit as st
import base64

def get_base64_image(image_path):
    """Reads a local image file and returns a base64 encoded string."""
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

def check_login_token():
    """
    Check login token with more robust persistence
    """
    # Check if login is already established in session state
    if st.session_state.get("logged_in"):
        return True
    
    # Check URL query parameter first
    token = st.query_params.get("token")
    
    # If token found in URL, set session state
    if token == "doctor":
        st.session_state["logged_in"] = True
        st.session_state["doctor"] = "Dr. Jane Doe"
        return True
    
    return False

# Redirects to Home after logout
def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.query_params.clear()
    st.switch_page("Home.py")

def ensure_login_token():
    """
    Ensures the login token is present in the URL
    """
    if st.session_state.get("logged_in") and "token" not in st.query_params:
        st.query_params["token"] = "doctor"

def show_navbar():
    """
    Displays a sidebar navbar with the app logo and the doctor profile.
    This should be called on every page when the user is logged in.
    """
    # Ensure login token is present
    ensure_login_token()
    
    if not st.session_state.get("logged_in"):
        return

    logo_img = get_base64_image("logo.jpeg")
    doctor_img = get_base64_image("doctor.jpeg")

    with st.sidebar:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="{doctor_img}" width="40" style="border-radius: 50%;">
            <h4 style="margin: 0;">{st.session_state.get('doctor', 'Doctor')}</h4>
        </div>
        <hr style="margin-top: 10px; margin-bottom: 10px;">
        """, unsafe_allow_html=True)

        if st.button("Logout"):
            logout()