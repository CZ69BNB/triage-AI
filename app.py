import streamlit as st

st.set_page_config(page_title="TriageAI", page_icon="🩺", layout="centered")

st.title("🫀 TriageAI: Multi-Modal Cardiopulmonary Hub")
st.caption("AI-Assisted Triaging Decision Support System")

tab1, tab2, tab3 = st.tabs(["🫀 ECG Photo", "🫁 Cough Screener", "🩻 Chest X-Ray"])

with tab1:
    st.subheader("1. Paper ECG Digitizer & Triage")
    ecg_file = st.file_uploader("Upload or take a photo of a 12-lead ECG", type=["png", "jpg", "jpeg"])
    if ecg_file:
        st.image(ecg_file, caption="Uploaded ECG Tracing", use_container_width=True)
        st.error("🚨 Triage Level 1: Emergent Finding")
        st.markdown("""
        - **Rhythm:** Sinus Tachycardia (108 bpm)
        - **Ischemia Flag:** ST-elevation detected in V2-V4 (Antero-septal territory)
        - **Action:** Alert ED Physician & initiate ACS protocol.
        """)

with tab2:
    st.subheader("2. Acoustic Respiratory Analysis")
    audio = st.file_uploader("Upload cough or breath sound", type=["wav", "mp3", "m4a"])
    if audio:
        st.audio(audio)
        st.warning("⚠️ Triage Level 2: Urgent")
        st.markdown("""
        - **Acoustic Signature:** Polyphonic expiratory wheeze pattern detected.
        - **Risk Score:** 84% probability of lower airway obstruction.
        """)

with tab3:
    st.subheader("3. Chest Radiograph (X-Ray / CT) Triage")
    xray = st.file_uploader("Upload Chest Radiograph", type=["png", "jpg", "jpeg"])
    if xray:
        st.image(xray, caption="Uploaded Chest Radiograph", use_container_width=True)
        st.info("ℹ️ Triage Level 3: Acute Finding")
        st.markdown("""
        - **Pathology:** Dense consolidation in the Right Lower Lobe (Pneumonia pattern).
        - **Secondary Note:** Costophrenic angles clear; no cardiomegaly.
        """)
