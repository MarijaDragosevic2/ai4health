import streamlit as st
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

st.set_page_config(page_title="Patient Directory", page_icon=img_logo, layout="wide")

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

show_navbar()


# --- Initialize selected patient state and view mode ---
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None
if "show_directory" not in st.session_state:
    st.session_state.show_directory = False
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# --- Load patient data from JSON file ---
@st.cache_data
def load_patients():
    with open("patients.json", "r") as f:
        return json.load(f)

def save_patients(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=2)

patients = load_patients()

# ---------------------------
# Directory View: List of Patients
# ---------------------------
if st.session_state.selected_patient is None:
    st.title("Patient Directory")
    st.markdown("Use the search bar to filter patients by ID or Name.")

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search by Patient ID or Name", value="")
        if search_term:
            filtered_patients = [
                p for p in patients 
                if search_term.lower() in p["id"].lower() or search_term.lower() in p["name"].lower()
            ]
        else:
            filtered_patients = patients

        if not filtered_patients:
            st.info("No patients found with that search term.")
        else:
            for patient in filtered_patients:
                if st.button(f"{patient['id']} - {patient['name']}", key=patient["id"]):
                    st.session_state.selected_patient = patient
                    st.session_state.show_directory = False
                    st.rerun()

# ---------------------------
# Detail View: Patient Selected
# ---------------------------
else:
    patient = st.session_state.selected_patient
    st.title(f"Patient: {patient['id']} - {patient['name']}")

    if st.button("Back to Patients"):
        st.session_state.selected_patient = None
        st.session_state.edit_mode = False
        st.rerun()

    # Show patient info table
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

    patient_info = {
        "Name": patient.get("name", ""),
        "Patient ID": patient.get("id", ""),
        "Age": patient.get("age", "N/A"),
        "Scan Date": patient.get("scan_date", "N/A"),
        "Radiologist": patient.get("radiologist", "N/A")
    }

    html_table = "<table class='custom-table'>"
    for key, value in patient_info.items():
        html_table += f"<tr><td>{key}</td><td>{value}</td></tr>"
    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)

    # Show image gallery below patient info in expandable section
    with st.expander("**View Mammo Images**"):
        cols = st.columns(4)
        for i, img_name in enumerate(patient.get("images", [])):
            image_path = os.path.join(".", img_name)
            with cols[i % 4]:
                if os.path.exists(image_path):
                    with open(image_path, "rb") as f:
                        st.image(f.read(), caption=f"Image {i+1}", use_container_width=True)
                else:
                    st.warning(f"Image not found: {img_name}")

    if not st.session_state.edit_mode:
        st.markdown("#### Medical History")
        st.write(patient.get("medical_history", "No medical history available."))

        st.markdown("#### Patient Record")
        st.write(patient.get("record", "No patient record available."))

        if st.button("Edit Data"):
            st.session_state.edit_mode = True
            st.rerun()

    else:
        st.markdown("#### Medical History")
        medical_history = st.text_area("Edit:", value=patient.get("medical_history", ""), height=100)

        st.markdown("#### Patient Record")
        record = st.text_area("Edit:", value=patient.get("record", ""), height=150)

        if st.button("💾 Save Changes"):
            patient["medical_history"] = medical_history
            patient["record"] = record

            for i, p in enumerate(patients):
                if p["id"] == patient["id"]:
                    patients[i] = patient
                    break

            save_patients(patients)
            st.session_state.selected_patient = patient
            st.session_state.edit_mode = False
            st.success("✅ Patient data updated and saved!")
            st.rerun()
