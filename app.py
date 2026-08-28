import streamlit as st
import pandas as pd

st.set_page_config(page_title="AbxGuard - Stewardship Engine", page_icon="💊", layout="wide")

st.title("💊 AbxGuard: Bedside Antimicrobial Stewardship Hub")
st.caption("Standardized Clinical Decision Support to Mitigate Antimicrobial Resistance (AMR)")

main_tab1, main_tab2, main_tab3 = st.tabs([
    "🩺 Empirical Triage & Renal Guard", 
    "📊 Institutional Antibiogram", 
    "⚠️ Drug-Drug Interaction Checker"
])

# ==========================================
# TAB 1: EMPIRICAL TRIAGE & RENAL DOSING
# ==========================================
with main_tab1:
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("1. Infection Profile & Triage")
        
        infection_site = st.selectbox(
            "Infection Category / Presentation",
            [
                "Upper Respiratory (Sore Throat / Pharyngitis)",
                "Community-Acquired Pneumonia (CAP)",
                "Uncomplicated Urinary Tract Infection (Cystitis)",
                "Skin & Soft Tissue (Cellulitis/Abscess)",
                "Acute Gastroenteritis (Suspected Infectious Diarrhea)"
            ]
        )
        
        viral_warning = False
        score_note = ""
        
        if "Pharyngitis" in infection_site:
            st.markdown("**Centor Score Criteria:**")
            c1 = st.checkbox("Absence of cough (+1)")
            c2 = st.checkbox("Swollen/tender anterior cervical nodes (+1)")
            c3 = st.checkbox("Temperature > 38°C (100.4°F) (+1)")
            c4 = st.checkbox("Tonsillar exudates (+1)")
            centor_score = sum([c1, c2, c3, c4])
            
            if centor_score <= 1:
                viral_warning = True
                score_note = f"Centor Score: {centor_score}/4 (High probability of Viral Etiology. Antibiotics NOT recommended)."
            else:
                score_note = f"Centor Score: {centor_score}/4 (Bacterial GAS likely. First-line targeted therapy indicated)."

        st.markdown("---")
        st.subheader("2. Renal Parameters (Cockcroft-Gault)")
        c_age, c_sex = st.columns(2)
        with c_age:
            age = st.number_input("Age (years)", min_value=18, max_value=100, value=48)
        with c_sex:
            gender = st.radio("Sex", ["Male", "Female"], horizontal=True)
            
        c_wt, c_cr = st.columns(2)
        with c_wt:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0, value=65.0)
        with c_cr:
            serum_cr = st.number_input("Serum Creatinine (mg/dL)", min_value=0.4, max_value=15.0, value=1.1, step=0.1)

        crcl = ((140 - age) * weight) / (72 * serum_cr)
        if gender == "Female":
            crcl *= 0.85
            
        st.info(f"**Calculated Creatinine Clearance (CrCl):** `{crcl:.1f} mL/min`")

    with col2:
        st.subheader("3. Recommended Empirical Regimen (WHO AWaRe)")
        
        if viral_warning:
            st.error("🚫 Antimicrobial Stewardship Alert: Antibiotic Sparing Recommended")
            st.write(f"**Clinical Score:** {score_note}")
            st.markdown("""
            * **Primary Therapy:** Symptomatic management (Hydration, Paracetamol, warm saline gargles).
            * **Rationale:** >85% of acute pharyngitis cases with Centor $\le 1$ are viral (Rhinovirus, Adenovirus, EBV).
            * **Safety Net:** Re-evaluate if symptoms persist past 5–7 days or dysphagia develops.
            """)
        else:
            if score_note:
                st.success(f"**Diagnostic Validation:** {score_note}")
                
            if "Pharyngitis" in infection_site:
                st.markdown("""
                * **WHO AWaRe:** 🟢 ACCESS
                * **First-Line Regimen:** **Amoxicillin** 500 mg PO TID or **Penicillin V** 500 mg PO QID
                * **Duration:** 10 days
                * **Alternative (Severe Beta-lactam allergy):** Azithromycin 500 mg Day 1, then 250 mg OD (Days 2–5) [🟡 WATCH]
                """)

            elif "Pneumonia" in infection_site:
                st.markdown("""
                * **WHO AWaRe:** 🟢 ACCESS + 🟡 WATCH
                * **Mild CAP Regimen:** **Amoxicillin** 500 mg – 1 g PO TID + **Clarithromycin** 500 mg PO BD (if atypical suspected)
                * **Duration:** 5 days
                """)
                if crcl < 30:
                    st.warning("⚠️ **Renal Adjustment:** Reduce Amoxicillin frequency to every 12 hours for CrCl < 30 mL/min.")

            elif "Cystitis" in infection_site:
                st.markdown("""
                * **WHO AWaRe:** 🟢 ACCESS (Narrow Spectrum)
                * **First-Line Option:** **Nitrofurantoin Monohydrate** 100 mg PO BD for 5 days OR **Fosfomycin** 3 g PO single dose
                """)
                if crcl < 30:
                    st.error("⚠️ **Renal Contraindication:** Nitrofurantoin is ineffective and risks neurotoxicity when CrCl < 30 mL/min. Switch to Fosfomycin or targeted agent.")

            elif "Cellulitis" in infection_site:
                st.markdown("""
                * **WHO AWaRe:** 🟢 ACCESS
                * **First-Line Regimen:** **Cefalexin** 500 mg PO QID or **Cloxacillin** 500 mg PO QID
                * **Duration:** 5 to 7 days
                """)

            elif "Gastroenteritis" in infection_site:
                st.warning("⚠️ **Stewardship Alert:** Acute diarrhea is self-limiting. Antibiotics are contraindicated unless frank dysentery or cholera is suspected.")
                st.markdown("""
                * **Primary Therapy:** Oral Rehydration Solution (ORS) + Zinc.
                * **Restricted Regimen (Dysentery only):** **Azithromycin** 500 mg PO OD for 3 days.
                """)

            st.markdown("---")
            st.subheader("4. Mandatory 72-Hour De-escalation Checklist")
            st.checkbox("Microbiology culture sample collected prior to first antibiotic dose")
            st.checkbox("72-hour clinical re-evaluation scheduled to switch IV to Oral")
            st.checkbox("Defined treatment stop date documented in clinical record")

# ==========================================
# TAB 2: INSTITUTIONAL ANTIBIOGRAM
# ==========================================
with main_tab2:
    st.subheader("📊 Hospital & Regional Susceptibility Patterns (ICMR / Local Hospital)")
    st.caption("Empirical choices should target agents with $\ge 80\%$ institutional susceptibility.")

    default_antibiogram = pd.DataFrame({
        "Pathogen": ["E. coli", "Klebsiella pneumoniae", "Pseudomonas aeruginosa", "Staph aureus (MRSA)", "Staph aureus (MSSA)"],
        "Amoxicillin-Clav": ["42%", "38%", "0% (Intrinsic)", "0%", "88%"],
        "Ceftriaxone": ["34%", "29%", "0% (Intrinsic)", "0%", "86%"],
        "Piperacillin-Tazo": ["72%", "68%", "82%", "0%", "92%"],
        "Meropenem": ["84%", "71%", "78%", "0%", "98%"],
        "Amikacin": ["88%", "81%", "85%", "N/A", "N/A"],
        "Nitrofurantoin": ["86%", "41%", "0% (Intrinsic)", "N/A", "N/A"],
        "Vancomycin": ["N/A", "N/A", "N/A", "100%", "100%"]
    })

    uploaded_file = st.file_uploader("Upload Custom Hospital Antibiogram (CSV)", type=["csv"])
    
    if uploaded_file:
        df_display = pd.read_csv(uploaded_file)
        st.success("Custom Hospital Antibiogram Loaded")
    else:
        df_display = default_antibiogram
        st.info("Displaying Benchmark National Surveillance Antibiogram Data")

    st.dataframe(df_display, use_container_width=True)

    st.markdown("""
    **Key Takeaways for Stewardship:**
    * **High ESBL burden in Gram-Negatives:** *E. coli* susceptibility to 3rd generation cephalosporins (Ceftriaxone) is $<40\%$. Reserve Ceftriaxone for confirmed culture-sensitive isolates.
    * **Urinary First-Line Preservation:** Nitrofurantoin maintains high susceptibility ($>85\%$) against *E. coli*, making it the preferred non-carbapenem oral agent for uncomplicated lower UTI.
    """)

# ==========================================
# TAB 3: DRUG-DRUG INTERACTION CHECKER
# ==========================================
with main_tab3:
    st.subheader("⚠️ Common Bedside Antimicrobial Interaction Checker")
    st.caption("Check for dangerous pharmacological synergies and QTc prolongation risks.")

    abx_choice = st.selectbox(
        "Select Prescribed Antimicrobial",
        [
            "Azithromycin / Clarithromycin (Macrolides)",
            "Ciprofloxacin / Levofloxacin (Fluoroquinolones)",
            "Amoxicillin-Clavulanate",
            "Doxycycline",
            "Linezolid",
            "Trimethoprim-Sulfamethoxazole (Cotrimoxazole)"
        ]
    )

    comeds = st.multiselect(
        "Select Concurrent Patient Medications",
        [
            "Warfarin (Oral Anticoagulant)",
            "Ondansetron (Antiemetic)",
            "Amiodarone (Antiarrhythmic)",
            "Antacids / Iron Supplements",
            "SSRIs (e.g., Fluoxetine, Sertraline)",
            "ACE Inhibitors / ARBs (e.g., Telmisartan)",
            "Statins (e.g., Atorvastatin)"
        ]
    )

    if st.button("Run Safety Cross-Check"):
        alerts = []
        
        if "Macrolides" in abx_choice or "Fluoroquinolones" in abx_choice:
            if "Ondansetron (Antiemetic)" in comeds or "Amiodarone (Antiarrhythmic)" in comeds:
                alerts.append("🔴 **Severe QTc Prolongation Risk:** Concomitant use with Ondansetron/Amiodarone elevates risk of Torsades de Pointes. Baseline ECG & telemetry monitoring required.")
            if "Statins (e.g., Atorvastatin)" in comeds and "Macrolides" in abx_choice:
                alerts.append("🟡 **CYP3A4 Inhibition (Myopathy Risk):** Clarithromycin significantly increases Atorvastatin plasma concentrations. Temporarily withhold statin during course.")

        if "Linezolid" in abx_choice and "SSRIs (e.g., Fluoxetine, Sertraline)" in comeds:
            alerts.append("🔴 **Fatal Serotonin Syndrome Warning:** Linezolid acts as a non-selective MAO inhibitor. Combined use with SSRIs is strictly contraindicated.")

        if "Cotrimoxazole" in abx_choice:
            if "ACE Inhibitors / ARBs (e.g., Telmisartan)" in comeds:
                alerts.append("🟡 **Severe Hyperkalemia Risk:** Trimethoprim exerts amiloride-like potassium-sparing effects in distal tubules. Monitor Serum Potassium closely.")
            if "Warfarin (Oral Anticoagulant)" in comeds:
                alerts.append("🔴 **Major Bleeding Alert:** Cotrimoxazole strongly inhibits Warfarin metabolism (CYP2C9). INR will surge; empirical Warfarin dose reduction by 50% required.")

        if "Doxycycline" in abx_choice or "Fluoroquinolones" in abx_choice:
            if "Antacids / Iron Supplements" in comeds:
                alerts.append("🟡 **Chelation & Absorption Failure:** Divalent/trivalent cations (Ca2+, Mg2+, Fe2+, Al3+) bind the antibiotic in the GI tract. Space administration by at least 2 hours.")

        if alerts:
            for a in alerts:
                st.markdown(a)
        else:
            st.success("✅ No major severe drug interactions flagged for this specific pair. Proceed with standard clinical monitoring.")
