import streamlit as st
from openai import OpenAI
import os

# Initialize local Ollama client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

st.set_page_config(page_title="EpiQual: Multi-Layer Outbreak Auditor", layout="wide")

st.title("📊 EpiQual: Outbreak Qualitative Data Assistant")
st.subheader("🔒 Multi-Layer Targeted Analysis Engine (Ollama Offline)")
st.markdown("---")

# Session state initialization for the active codebook and analysis outputs
if 'codebook' not in st.session_state:
    st.session_state.codebook = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = ""

# --- LAYER 0: METHODOLOGY CONFIGURATION ---
QUAL_APPROACHES = {
    "Deductive / Framework Analysis (Direct Coding)": (
        "Analyze the transcript strictly using the active codebook definitions. "
        "Do not invent new themes. Act as a literal, structured auditor looking "
        "exclusively for predefined framework indicators."
    ),
    "Inductive / Grounded Theory (Emergent Coding)": (
        "Disregard strict boundaries. Let the data speak first. Focus on discovering "
        "new, raw, community-derived themes, local behavioral workarounds, "
        "socio-economic stressors, and unexpected operational realities not captured by formal global frameworks."
    ),
    "Hybrid (Combined Deductive-Inductive)": (
        "First, map the narrative to the active framework codebook. Second, actively identify "
        "and isolate emergent codes (emerging local anomalies, cultural beliefs, and field realities) "
        "that fall outside of the formal frameworks but heavily impact the outbreak dynamics."
    )
}

# --- LAYER 1: OUTBREAK CLUSTER DEFINITIONS ---
OUTBREAK_CLUSTERS = [
    "Zoonotic Diseases (One Health Context)",
    "Vaccine-Preventable Diseases (VPDs)",
    "Influenza-Like Illnesses (ILI) / Respiratory Pathogens",
    "Food and Water-Borne Diseases (FWBD)",
    "Chemical, Biological, Radiological, and Nuclear (CBRN) Incidents",
    "Crisis, Disasters, and Climate-Induced Emergencies",
    "Emerging and Re-emerging Infectious Diseases (EIDs)"
]

# --- LAYER 2: SYSTEMATIC FRAMEWORK METADATA ---
FRAMEWORK_DATABASE = {
    "7-1-7 Framework (Granular Targets & Response Actions)": {
        "D1: Clinical Suspicion & Community Case Search (Detect)": "Bottlenecks in clinician awareness, community event-based monitoring, or health-seeking delays that prevent detecting the outbreak within 7 days of emergence.",
        "D2: Diagnostic Routing & Local Testing (Detect)": "Delays in recognizing clusters at the facility level, lack of local testing capacity, or transport barriers for initial clinical samples during the detection window.",
        "N1: Facility-to-LGU Data Transmission (Notify)": "Technical failure of electronic reporting tools (e.g., PIDSR/surveillance portals), phone connectivity issues, or administrative delays in notifying local public health offices within 1 day.",
        "N2: National & International Reporting (Notify)": "Bureaucratic delays or fear of economic/political repercussions that stall official notification to higher ministry levels or International Health Regulations (IHR) focal points.",
        "R1: Deploy Investigation Teams (Respond)": "Failure or delay in mobilising and sending out rapid response teams (RRTs) to the epicenter of the outbreak.",
        "R2: Conduct Epi Analysis & Risk Assessment (Respond)": "Delays in completing line lists, tracking secondary cases, analyzing risk factors, or establishing the initial risk assessment profile.",
        "R3: Obtain Lab Confirmation (Respond)": "Logistical bottlenecks in sending samples to reference laboratories, reagent stockouts, or long laboratory turnaround times.",
        "R4: Initiate Case Management & Facility IPC (Respond)": "Inadequate clinical care protocols, lack of isolation wards, or failures in Infection Prevention and Control (IPC) that lead to healthcare-associated transmission.",
        "R5: Initiate Public Health Countermeasures (Respond)": "Delays in launching community-level interventions such as vector control, distribution of clean water, vaccine campaigns, or sanitation measures.",
        "R6: Launch Risk Communication & RCCE (Respond)": "Failure to deploy timely, culturally appropriate risk communications, address public panic, manage misinformation, or engage community leaders.",
        "R7: Establish Coordination Mechanisms (Respond)": "Breakdown in setting up Incident Command Systems (ICS), coordinating multi-agency responders, or activating emergency operations centers."
    },
    "PopCAB (Population Connectivity Across Borders)": {
        "Mobility Pathways & Hubs": "Failure to identify major transport corridors, informal border crossing points, transit hubs, or seasonal migration routes that facilitate rapid disease spread.",
        "Point of Entry (POE) Surveillance Gaps": "Inadequate screening, lack of isolation spaces, or absent health declarations at official airports, seaports, or land-border checkpoints.",
        "Cross-Border Health Information Sharing": "Absence of data-sharing agreements, delayed communication, or incompatible surveillance systems between adjacent jurisdictions or neighboring countries.",
        "Migrant & Mobile Population Barriers": "Marginalization, language barriers, lack of legal status, or fear of deportation that prevents travelers and migrants from accessing healthcare or cooperating with contact tracers.",
        "Multi-Jurisdictional Response Gaps": "Conflicting local/national emergency protocols, lack of joint cross-border simulation exercises, or uncoordinated containment measures across regional boundaries.",
        "Spatial Transmission Hotspots": "Inability to map or account for highly connected locations (e.g., cross-border markets, religious festivals, shared workplaces) that act as super-spreader nodes."
    },
    "CDC Surveillance System Attributes (Gaps)": {
        "Simplicity Barriers": "The system is too complex, has excessively redundant forms, or requires tedious workflow steps that discourage frontline health workers from reporting cases.",
        "Acceptability & Reporting Gaps": "Frontline personnel, clinicians, or LGUs refuse or are hesitant to participate in reporting due to administrative burden, lack of feedback, or fear of punitive action.",
        "Data Quality & Completeness Issues": "High rates of missing variables in case investigation forms, inconsistent application of standard case definitions, or poor data entry protocols.",
        "Sensitivity & Under-reporting Gaps": "The surveillance system fails to capture true positive cases, missing community-level clusters or failing to detect early warning signals of an outbreak.",
        "Representativeness Gaps": "Failure of the surveillance system to capture marginalized communities, remote geographic areas, or private healthcare sector cases, leading to a biased epidemiological picture.",
        "Stability & System Downtime": "Frequent crashes of electronic databases, power/internet outages, or sudden turnover of trained epidemiological staff interrupting continuous surveillance operations.",
        "Flexibility Gaps": "Inability of the surveillance system to quickly adapt to emerging pathogens, changes in case definitions, or sudden modifications in reporting procedures."
    },
    "Asia Pacific Health Security Action Framework (APHSAF)": {
        "Domain 1: Lead and Coordinate": "Gaps or delays in leadership, governance partnerships, multisectoral coordination (including One Health coordination), and regional/international information-sharing.",
        "Domain 2: Plan and Prepare": "Deficiencies in legal/regulatory frameworks, national health security planning, system preparedness, or health information/forecasting systems.",
        "Domain 3: Assess and Respond": "Bottlenecks in multisource surveillance, laboratory system diagnostic capacity, biosafety, sample transport, or rapid response deployment.",
        "Domain 4: Readiness and Resilience": "Failures in community-level prevention/risk reduction, delivery of essential and emergency healthcare, or prioritizing measures for vulnerable populations.",
        "Domain 5: Support and Enable": "Systemic challenges in developing/sustaining the health security workforce, mobilizing rapid finance, optimizing logistics/supply chains, or leveraging research and technology.",
        "Domain 6: Monitor, Evaluate and Improve": "Inadequacies in regular capacity assessments, conducting simulation exercises to test emergency plans, or synthesizing lessons learned to adapt and improve."
    },
    "One Health Joint Plan of Action (OH JPA 2022–2026)": {
        "Track 1: One Health Capacity & Health Systems": "Gaps in multisectoral health system capacity, cross-training of medical/veterinary/environmental workforces, and joint emergency response planning.",
        "Track 2: Emerging Zoonotic Epidemics & Spillover": "Issues with predicting, monitoring, and managing spillover events at the human-animal interface, and surveillance of wild and domestic animal populations.",
        "Track 3: Endemic Zoonotic, Neglected Tropical & Vector-Borne Diseases": "Failures in addressing long-standing endemic zoonoses (e.g., rabies, brucellosis) or vector-borne illnesses using community-centric, multisectoral interventions.",
        "Track 4: Food Safety & Food Systems Risks": "Breakdowns in managing chemical/microbiological contamination, animal slaughter inspections, or wet-market safety standards along the food supply chain.",
        "Track 5: Antimicrobial Resistance (AMR) Mitigation": "Inadequate control of antibiotics usage in livestock, lack of cross-sectoral AMR surveillance, or agricultural runoff containing active antimicrobials.",
        "Track 6: Environmental Integration & Biodiversity": "Failure to address climate change impacts, ecosystem degradation, deforestation, wildlife trade, and environmental toxins that drive spillover and vulnerability."
    },
    "WHO Health-EDRM Framework (Crisis Management)": {
        "Component 1: Policies, Planning & Coordination": "Fragmented command structures, misalignment of national/local response plans, or breakdown in the multi-agency Incident Command System (ICS).",
        "Component 2: Information Management & Risk Communication": "Failures in active risk monitoring, delayed early warning alerts, broken situational reporting, or mismanaged public crisis messaging.",
        "Component 3: Health Infrastructure & Logistics": "Supply chain and logistical bottlenecks, lack of critical medical/PPE stockpiles, and unsafe or physically overwhelmed frontline healthcare facilities.",
        "Component 4: Health Services & Surge Capacity": "Deficiencies in clinical surge capacity, lack of deployed Emergency Medical Teams (EMTs), or breakdown in essential/routine healthcare delivery during emergencies.",
        "Component 5: Human & Financial Resources": "Systemic shortages of trained emergency responders, inadequate occupational health/safety measures, or delays in mobilizing emergency/contingency funds.",
        "Component 6: Community Capacities & Vulnerability": "Failure to utilize localized disaster plans, lack of engagement with community leaders, or failure to safeguard highly vulnerable, marginalized, or displaced populations."
    }
}

# --- SIDEBAR: FRAMEWORK TARGETING ---
st.sidebar.header("🔬 1. Qualitative Methodology")
selected_approach = st.sidebar.selectbox("Choose Qualitative Lens:", list(QUAL_APPROACHES.keys()))
st.sidebar.info(f"**Methodological Guide:** {QUAL_APPROACHES[selected_approach]}")

st.sidebar.markdown("---")
st.sidebar.header("🦠 2. Target the Investigation")

selected_outbreak = st.sidebar.selectbox("Select Outbreak Cluster:", OUTBREAK_CLUSTERS)
selected_framework = st.sidebar.selectbox("Select Evaluation Framework:", list(FRAMEWORK_DATABASE.keys()))
available_themes = FRAMEWORK_DATABASE[selected_framework]

st.sidebar.markdown(f"**Select specific themes from {selected_framework}:**")
selected_subthemes = []
for theme_name in available_themes.keys():
    if st.sidebar.checkbox(theme_name, key=f"chk_{theme_name}"):
        selected_subthemes.append(theme_name)

if st.sidebar.button("📥 Load Framework into Active Codebook"):
    if not selected_subthemes:
        st.sidebar.warning("Please check at least one framework theme.")
    else:
        for theme in selected_subthemes:
            st.session_state.codebook[theme] = {
                "description": available_themes[theme],
                "type": "Standard Framework Code"
            }
        st.sidebar.success(f"Loaded {len(selected_subthemes)} codes focused on {selected_outbreak}!")

st.sidebar.markdown("---")
st.sidebar.markdown("### ➕ Add Emergent Custom Codes")
with st.sidebar.form("add_custom_code_form", clear_on_submit=True):
    custom_code_name = st.text_input("Custom Code/Theme Name")
    custom_code_desc = st.text_area("Operational Definition")
    submit_custom = st.form_submit_button("Add Custom Code")
    if submit_custom and custom_code_name and custom_code_desc:
        st.session_state.codebook[custom_code_name] = {
            "description": custom_code_desc,
            "type": "Emergent Custom Code"
        }
        st.sidebar.success(f"Added custom emergent code: {custom_code_name}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Active Evaluation Framework:")
if not st.session_state.codebook:
    st.sidebar.info("Codebook is empty. Load themes above.")
else:
    st.sidebar.markdown(f"**Target Scenario:** `{selected_outbreak}`")
    for code, data in st.session_state.codebook.items():
        badge = "⚙️ Custom" if data["type"] == "Emergent Custom Code" else "🏛️ System"
        st.sidebar.markdown(f"**{code}** ({badge}): *{data['description']}*")
    
    if st.sidebar.button("🗑️ Clear Active Codebook"):
        st.session_state.codebook = {}
        st.rerun()


# --- MAIN PANEL: MULTI-TAB WORKSPACE ---
tab1, tab2, tab3 = st.tabs(["🎙️ Step 1: Ingest Narratives", "🤖 Step 2: Thematic Audit", "📊 Step 3: Evaluation & Usability Sandbox"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Field Media Processing")
        
        # FIXED: Modified to allow video file formats (.mp4, .mkv, .mov) alongside audio
        uploaded_file = st.file_uploader(
            "Upload field recording (.mp3, .wav, .m4a, .mp4, .mkv, .mov)", 
            type=["mp3", "wav", "m4a", "mp4", "mkv", "mov"]
        )
        extracted_text = ""
        
        if uploaded_file is not None:
            # Check file extension to render the correct media player preview
            file_extension = os.path.splitext(uploaded_file.name)[-1].lower()
            if file_extension in [".mp4", ".mkv", ".mov"]:
                st.video(uploaded_file)
            else:
                st.audio(uploaded_file)
                
            if st.button("Transcribe Media (Local Run)"):
                with st.spinner("Processing media text extraction locally..."):
                    try:
                        from faster_whisper import WhisperModel
                        with open("temp_media_file", "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # whisper processes audio tracks out of container files seamlessly
                        model = WhisperModel("small", device="cpu", compute_type="int8")
                        segments, info = model.transcribe("temp_media_file", beam_size=5)
                        extracted_text = " ".join([segment.text for segment in segments])
                        st.success(f"Successfully processed! Detected language: {info.language}")
                        os.remove("temp_media_file")
                    except Exception as e:
                        st.error(f"Local transcription error: {e}")
                        if os.path.exists("temp_media_file"):
                            os.remove("temp_media_file")
                        
    with col2:
        st.subheader("Transcript Workspace")
        transcript_input = st.text_area(
            "Paste or Edit Field Narratives Below:",
            value=extracted_text if extracted_text else "",
            height=300,
            placeholder="Paste raw field interview transcripts..."
        )

with tab2:
    st.subheader("Targeted Thematic Audit Engine")
    st.markdown("Initiates the qualitative analysis of the narratives in the workspace based on your sidebar specifications.")
    
    if st.button("Run Targeted Framework Analysis", type="primary"):
        if not st.session_state.codebook:
            st.warning("Your active codebook framework is empty. Please configure and load options in the sidebar.")
        elif not transcript_input:
            st.warning("Please provide transcript data in Step 1 first.")
        else:
            with st.spinner("Analyzing text through targeted local AI modules..."):
                formatted_codes = ""
                for code, data in st.session_state.codebook.items():
                    formatted_codes += f"- Code Name: {code}\n  Definition: {data['description']}\n\n"
                
                system_prompt = (
                    f"You are an elite qualitative public health research assistant auditing field data from a recent outbreak investigation.\n"
                    f"CONTEXT OF ANALYSIS: This investigation evaluates a [{selected_outbreak}] event.\n\n"
                    f"REQUIRED METHODOLOGICAL APPROACH: [{selected_approach}]\n"
                    f"INSTRUCTION FOR APPROACH: {QUAL_APPROACHES[selected_approach]}\n\n"
                    "CRITICAL ASSIGNMENT:\n"
                    "Read the provided qualitative transcript. Locate and categorize segments matching your operational directives.\n\n"
                    f"ACTIVE FRAMEWORK CODEBOOK (Use if/as dictated by the selected methodological approach):\n{formatted_codes}\n"
                    "OUTPUT FORMAT REQUIREMENT:\n"
                    "For every theme or code detected in the transcript, you MUST return the results matching this exact structured format:\n\n"
                    "### 📌 [Insert Theme/Code Name Here]\n"
                    "- **Verbatim Narrative Context (Exact Quote):** \"[Insert the exact raw word-for-word string from the text. Keep it in its original language, like Tagalog/Taglish/Cebuano/Chavacano. Do not change punctuation or words.]\"\n"
                    "- **Epidemiological Bottleneck Memo:** [Provide a concise, 2-sentence analytical summary of what systemic error, operational delay, or coordination block this quote represents under the chosen context.]\n\n"
                    "If the chosen approach requires generating emergent, inductive codes, format them the exact same way but add a '🌱 [Emergent Grounded Code]' tag next to the theme name.\n"
                    "If a theme or code is not detected, do not list it. Be extremely objective. Do not extrapolate outside the text."
                )
                
                try:
                    response = client.chat.completions.create(
                        model="llama3.1",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Transcript to process:\n\"\"\"{transcript_input}\"\"\""}
                        ],
                        temperature=0.1
                    )
                    st.session_state.analysis_results = response.choices[0].message.content
                except Exception as e:
                    st.error(f"Ollama local model link failed: {e}")
                    
    if st.session_state.analysis_results:
        st.markdown("### 📋 Generated Audit Output")
        st.markdown(st.session_state.analysis_results)
        st.download_button(
            label="💾 Download Audit Report (.txt)",
            data=st.session_state.analysis_results,
            file_name="targeted_outbreak_qual_report.txt",
            mime="text/plain"
        )
    else:
        st.info("No analysis run yet. Proceed to run the analysis above.")

with tab3:
    st.header("📊 EpiQualApp Effectiveness & Usability Evaluation Sandbox")
    st.markdown("Deploy this dashboard feature to gather standard usability metrics and public health utility feedback from field evaluators.")
    
    st.markdown("---")
    
    # --- EVALUATION FORM ---
    with st.form("epiqual_usability_form"):
        st.subheader("Part I: System Usability Scale (SUS) Metrics")
        st.caption("Please rate each usability statement from 1 (Strongly Disagree) to 5 (Strongly Agree).")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            sus_q1 = st.slider("1. I would like to use EpiQual frequently in my outbreak investigations.", 1, 5, 3)
            sus_q3 = st.slider("3. I thought the application was intuitive and easy to use.", 1, 5, 3)
            sus_q5 = st.slider("5. I found the various functions well-integrated.", 1, 5, 3)
            sus_q7 = st.slider("7. I imagine most field epidemiologists would learn this system quickly.", 1, 5, 3)
            sus_q9 = st.slider("9. I felt highly confident utilizing the generated reports.", 1, 5, 3)
        with col_s2:
            sus_q2 = st.slider("2. I found the interface and sidebar controls unnecessarily complex.", 1, 5, 3)
            sus_q4 = st.slider("4. I would need the support of a technical person to use this app.", 1, 5, 3)
            sus_q6 = st.slider("6. I thought there was too much inconsistency in formatting.", 1, 5, 3)
            sus_q8 = st.slider("8. I found the workflow from transcription to audit cumbersome.", 1, 5, 3)
            sus_q10 = st.slider("10. I needed to learn complex AI prompting before using this app.", 1, 5, 3)
            
        st.markdown("---")
        st.subheader("Part II: Public Health Utility & Qualitative Rigor")
        st.caption("Rate the utility of these analytical sub-modules from 1 (Poor/Inaccurate) to 5 (Outstanding/Extremely Accurate).")
        
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            util_717 = st.selectbox("7-1-7 Granular Target Mapping:", [1, 2, 3, 4, 5], index=2)
            util_popcab = st.selectbox("PopCAB Cross-Border Ingestion Utility:", [1, 2, 3, 4, 5], index=2)
            util_cdc = st.selectbox("CDC Surveillance System Gaps Detection:", [1, 2, 3, 4, 5], index=2)
        with col_u2:
            util_verbatim = st.selectbox("Verbatim Narrative Preservation (Low/No Hallucination):", [1, 2, 3, 4, 5], index=2)
            util_dialect = st.selectbox("Comprehension of Regional Dialects (Tagalog/Chavacano/etc.):", [1, 2, 3, 4, 5], index=2)
            util_security = st.selectbox("Offline Processing & Data Privacy Security:", [1, 2, 3, 4, 5], index=2)
            
        st.markdown("---")
        st.subheader("Part III: Narrative Field Feedback")
        evaluation_notes = st.text_area(
            "Provide any general feedback, observed functional gaps, or recommendations for next deployments:",
            placeholder="Type any additional remarks here..."
        )
        
        submit_eval = st.form_submit_button("Calculate & Compile Evaluation Report", type="primary")
        
    if submit_eval:
        # Calculate standard SUS Score
        # Odd Qs (1, 3, 5, 7, 9) contribute score - 1
        pos_score = (sus_q1 - 1) + (sus_q3 - 1) + (sus_q5 - 1) + (sus_q7 - 1) + (sus_q9 - 1)
        # Even Qs (2, 4, 6, 8, 10) contribute 5 - score
        neg_score = (5 - sus_q2) + (5 - sus_q4) + (5 - sus_q6) + (5 - sus_q8) + (5 - sus_q10)
        sus_total = (pos_score + neg_score) * 2.5
        
        st.success("🎉 Evaluation Scorecard Successfully Generated!")
        
        # Display Metrics
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Calculated System Usability Scale (SUS) Score", value=f"{sus_total}/100")
            if sus_total >= 80.3:
                st.balloons()
                st.write("🟢 **Adjective Rating:** Excellent / Grade A")
            elif sus_total >= 68:
                st.write("🟡 **Adjective Rating:** Acceptable / Grade C")
            else:
                st.write("🔴 **Adjective Rating:** Marginally Poor / Grade F (Needs Redesign)")
                
        with col_m2:
            utility_avg = (util_717 + util_popcab + util_cdc + util_verbatim + util_dialect + util_security) / 6.0
            st.metric(label="Epidemiological Framework Utility Average", value=f"{utility_avg:.2f}/5.0")
            
        # Format Compile Report payload
# Format Compile Report payload using robust triple quotes
        compiled_report = f"""=== EPIDUALAPP EVALUATION SCORECARD ===
Qualitative Methodology Evaluated: {selected_approach}
Epidemiological Target Domain: {selected_outbreak}
Systematic Framework Used: {selected_framework}

--- PART I: USABILITY METRICS ---
Calculated SUS Score: {sus_total}/100
Individual Items:
  - Q1 (Use Frequency): {sus_q1}/5
  - Q2 (Unnecessary Complexity): {sus_q2}/5
  - Q3 (Intuitive/Ease of Use): {sus_q3}/5
  - Q4 (Technical Support Needed): {sus_q4}/5
  - Q5 (Well-Integrated Functions): {sus_q5}/5
  - Q6 (Inconsistent Formatting): {sus_q6}/5
  - Q7 (Quick Learnability): {sus_q7}/5
  - Q8 (Cumbersome Workflow): {sus_q8}/5
  - Q9 (Report Confidence Utility): {sus_q9}/5
  - Q10 (AI Prompt Barrier): {sus_q10}/5

--- PART II: PUBLIC HEALTH UTILITY METRICS ---
Average Score: {utility_avg:.2f}/5.0
  - 7-1-7 Core Targets Mapping: {util_717}/5
  - PopCAB Cross-Border Ingestion: {util_popcab}/5
  - CDC Surveillance System Gaps: {util_cdc}/5
  - Verbatim Quote Integrity: {util_verbatim}/5
  - Dialect Comprehension Level: {util_dialect}/5
  - Local Air-Gapped Security: {util_security}/5

--- PART III: EVALUATOR REMARKS ---
Comments:
"{evaluation_notes if evaluation_notes else 'No additional remarks provided.'}"
"""