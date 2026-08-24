import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="TriageAI", page_icon="🩺", layout="centered")

st.title("🫀 TriageAI: Multi-Modal Cardiopulmonary Hub")
st.caption("AI-Assisted Triaging Decision Support System")

# Sidebar for API key input
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.caption("Get a free key from Google AI Studio")

tab1, tab2, tab3 = st.tabs(["🫀 ECG Photo", "🫁 Cough Screener", "🩻 Chest X-Ray"])

with tab1:
    st.subheader("1. Paper ECG Digitizer & Triage")
    ecg_file = st.file_uploader("Upload or take a photo of a 12-lead ECG", type=["png", "jpg", "jpeg"])
    
    if ecg_file:
        img = Image.open(ecg_file)
        st.image(img, caption="Uploaded ECG Tracing", use_container_width=True)
        
        if st.button("Run AI Clinical Interpretation", key="ecg_btn"):
            if not api_key:
                st.warning("Please enter your Gemini API Key in the sidebar to run live analysis.")
            else:
                with st.spinner("Analyzing ECG trace and clinical parameters..."):
                    client = genai.Client(api_key=api_key)
                    prompt = """
                    You are an expert cardiologist AI. Analyze this 12-lead paper ECG image carefully:
                    1. Read printed header values (Heart Rate, intervals, patient info if present).
                    2. Check rhythm, rate, axis, PR interval, QRS complex, and ST-T segments across all leads.
                    3. Determine the Triage Level: (Level 1: Emergent / Level 2: Urgent / Level 3: Non-urgent / Normal).
                    4. Provide a structured concise summary: Rhythm & Rate, Morphological Findings, Primary Impression, Recommended Action.
                    """
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[prompt, img]
                    )
                    st.markdown("### AI Diagnostic Report")
                    st.write(response.text)

with tab2:
    st.subheader("2. Acoustic Respiratory Analysis")
    audio = st.file_uploader("Upload cough or breath sound", type=["wav", "mp3", "m4a"])
    if audio:
        st.audio(audio)
        st.info("Acoustic Model: Ready for audio classification.")

with tab3:
    st.subheader("3. Chest Radiograph (X-Ray / CT) Triage")
    xray_file = st.file_uploader("Upload Chest Radiograph", type=["png", "jpg", "jpeg"])
    if xray_file:
        xray_img = Image.open(xray_file)
        st.image(xray_img, caption="Uploaded Radiograph", use_container_width=True)
        if st.button("Analyze Radiograph", key="xray_btn"):
            if not api_key:
                st.warning("Please enter your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Screening radiograph for acute findings..."):
                    client = genai.Client(api_key=api_key)
                    prompt = "Analyze this chest radiograph. Identify any consolidations, infiltrates, pleural effusion, pneumothorax, or cardiomegaly. Give a triage score and clinical impression."
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[prompt, xray_img]
                    )
                    st.markdown("### Radiographic Findings")
                    st.write(response.text)
