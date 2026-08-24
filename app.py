import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="TriageAI", page_icon="🩺", layout="centered")

st.title("🫀 TriageAI: Multi-Modal Cardiopulmonary Hub")
st.caption("AI-Assisted Triaging Decision Support System")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.caption("Get a free key from Google AI Studio")

def get_best_model():
    # Automatically finds the supported vision model available on your key
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if 'flash' in m.name or 'pro' in m.name:
                return m.name
    return 'models/gemini-1.5-flash-latest'

tab1, tab2, tab3 = st.tabs(["🫀 ECG Photo", "🫁 Cough Screener", "🩻 Chest X-Ray"])

with tab1:
    st.subheader("1. Paper ECG Digitizer & Triage")
    ecg_file = st.file_uploader("Upload or take a photo of a 12-lead ECG", type=["png", "jpg", "jpeg"])
    
    if ecg_file:
        img = Image.open(ecg_file)
        st.image(img, caption="Uploaded ECG Tracing", use_container_width=True)
        
        if st.button("Run AI Clinical Interpretation", key="ecg_btn"):
            if not api_key:
                st.warning("Please enter your Gemini API Key in the sidebar.")
            else:
                with st.spinner("Analyzing ECG trace and clinical parameters..."):
                    try:
                        genai.configure(api_key=api_key)
                        model_name = get_best_model()
                        model = genai.GenerativeModel(model_name)
                        
                        prompt = """
                        You are an expert clinical triage assistant. Analyze this 12-lead paper ECG image carefully:
                        1. Extract header details if legible (Heart rate, patient demographics).
                        2. Analyze the rhythm, rate, intervals (PR, QRS, QT), and ST-T segment morphology.
                        3. Determine the Triage Level: (Level 1: Emergent / Level 2: Urgent / Level 3: Non-urgent / Normal).
                        4. Provide a structured clinical report: 
                           - **Rate & Rhythm**
                           - **Lead-by-Lead Observations**
                           - **Primary Impression**
                           - **Recommended Triage Action**
                        """
                        response = model.generate_content([prompt, img])
                        st.markdown("### 📋 AI Diagnostic Report")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error processing request: {e}")

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
                    try:
                        genai.configure(api_key=api_key)
                        model_name = get_best_model()
                        model = genai.GenerativeModel(model_name)
                        
                        prompt = """
                        Analyze this chest radiograph. Check for consolidations, infiltrates, pleural effusion, pneumothorax, or cardiomegaly. 
                        Provide a triage urgency rating and structured clinical findings.
                        """
                        response = model.generate_content([prompt, xray_img])
                        st.markdown("### 🩻 Radiographic Findings")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error processing request: {e}")
