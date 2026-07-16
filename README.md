# 📊 EpiQual: Local Outbreak & Qualitative Data Assistant

EpiQual is a privacy-first, custom AI-assisted qualitative data coding and audio transcription tool built for epidemiological and public health research in the Philippines. It allows researchers and students to transcribe raw field audio and analyze text using targeted global outbreak evaluation frameworks—**100% offline, free, and locally on your machine** using Ollama and local Whisper.

---

## 🛠️ Prerequisites

Before running the application, make sure you have the following installed on your computer:

1. **Python (v3.10 or higher)**: Download from [python.org](https://www.python.org/downloads/). 
   * *Important for Windows users:* Check the box that says **"Add python.exe to PATH"** during installation.
2. **Visual Studio Code (VS Code)**: Download from [code.visualstudio.com](https://code.visualstudio.com/).
3. **Ollama**: Download from [ollama.com](https://ollama.com/). This runs the Large Language Model engine locally.

---

## 🚀 Setup Instructions

Follow these step-by-step instructions to get the application running on your local machine:

### Step 1: Download the Local AI Model
Open your computer's regular command prompt (Windows) or terminal (Mac) and download the Llama model by running:
```bash

ollama pull llama3.1

Note for students with older/slower laptops (less than 16GB RAM): If the app runs slowly, download the lighter 3-billion parameter model instead:
```bash

ollama pull llama3.2:3b

(If you download Llama 3.2, make sure to change line 147 in your app.py file from model="llama3.1" to model="llama3.2:3b").

Keep the Ollama application running in the background while using the app.

Step 2: Open the Project in VS Code
Open VS Code.

Go to File > Open Folder... and select your EpiQualApp folder.

Open the built-in terminal in VS Code (Terminal > New Terminal at the top menu).

Step 3: Install Required Dependencies
In the VS Code terminal, run the following command to install the necessary library packages for the dashboard, the AI framework, and local audio transcription:
```bash

python -m pip install streamlit openai faster-whisper

🏃 How to Run the App
Once setup is complete, execute the following command in your VS Code terminal to launch the interface:
``bash

python -m streamlit run app.py --client.toolbarMode=hidden

Note: A browser window will automatically open at http://localhost:8501 to display your EpiQual workspace.

##################################### INSTRUCTIONS #############################################
📖 How to Use the EpiQual App (Step-by-Step)
# To analyze qualitative outbreak data with targeted precision, guide your workflow using the following steps:

### Step 1: Align Your Outbreak Context & Framework (Sidebar)
Before inputting data, you must configure your research scope in the left sidebar:

Select Outbreak Cluster: Choose the type of health emergency scenario you are auditing (e.g., Zoonotic Diseases, Vaccine-Preventable Diseases, or Food and Water-Borne Diseases).

Select Evaluation Framework: Pick an international public health evaluation standard:

7-1-7 Framework: Focuses strictly on the timeliness of early detection, notification, and response.

APSED III / IHR (2005): Targets surveillance, laboratory systems, emergency preparedness, and risk communication.

One Health Approach: Pinpoints gaps at the human-animal-environmental interface.

Health-EDRM: Looks at Incident Command System (ICS) failures, resource bottlenecks, and community vulnerability.

Load Codes: Check the boxes for the specific thematic sub-codes you want to audit, then click the "Load Framework into Active Codebook" button.

### Step 2: Add Emergent Custom Codes (Optional)
If your qualitative transcripts contain unique local anomalies, community-specific contexts, or themes not represented in the standard global frameworks:

Scroll down the sidebar to "Add Emergent Custom Codes".

Input a Code Name and an Operational Definition describing what you are looking for.

Click "Add Custom Code". This appends your custom criteria dynamically into your active codebook.

### Step 3: Ingest Field Narratives

In the main panel, navigate to **Step 1: Ingest Narratives** to feed raw outbreak data into your analytical workspace. The app supports three flexible ingestion pathways:

* **Method A: Direct File Upload (Best for smaller media)**
  For lightweight audio or video files under 15MB, drop your file (`.mp3`, `.wav`, `.m4a`, `.mp4`, `.mkv`, or `.mov`) directly into the browser uploader. Click **"Transcribe Media (Local Run)"** to run the offline Whisper engine.
  
* **Method B: Local File Path (Recommended for large files)**
  For massive recordings or video files, avoid network lag and memory spikes by pasting the absolute local file path (e.g., `C:\Users\Username\Videos\interview_01.m4a`) directly into the text input. The Whisper engine will stream and transcribe the file directly from your hard drive with zero upload overhead.

* **Method C: Direct Text Paste**
  If you already have pre-written transcripts, notes, or rapid qualitative assessments, skip transcription entirely and paste them directly into the interactive **Transcript Workspace** panel on the right.

> 🇵🇭 **Localization Note:** The underlying AI model natively decodes mixed-language transcripts (Taglish), core regional Philippine dialects (including Tagalog, Cebuano, and Chavacano), and colloquial community health idioms without losing critical epidemiological context.

### Step 4: Run Targeted Framework Analysis
Scroll to the bottom of the right panel and click the primary "Run Targeted Framework Analysis" button.

The offline AI model will audit your transcripts, searching for evidence that matches your active codebook.

Verbatim & Analytical Outputs: For every code identified, the AI will output:

📌 The Code/Theme Name

💬 Verbatim Narrative Context: The exact raw, word-for-word quote extracted from the transcript in its original dialect (preserving local context like sumpong, pasiyam, or hilot).

📝 Epidemiological Bottleneck Memo: A concise, 2-sentence analytical translation of the systemic error or logistical delay this quote represents.

### Step 5: Export Your Report
Once the analysis is displayed on your screen, click the "Download Analysis Report (.txt)" button. This saves your structured qualitative output as a text file, ready to be incorporated into your outbreak evaluation report or academic project.

🔒 Data Privacy & Compliance Note
Because this application runs entirely locally using your machine's hardware via Ollama and a local instance of Whisper, no data is transmitted over the internet or sent to third-party cloud servers. This architecture complies with standard public health research ethics requirements regarding the processing of sensitive participant narratives.

################################ RUN DEMO1 ###################################
SCENARIO: Cross-Border Mpox (Clade 1b)
The Scenario: A highly mobile trader traveling back and forth across a maritime border (e.g., between Sabah, Malaysia, and Tawi-Tawi/Sulu, Philippines) via informal ports, carrying suspected Mpox with classic lesions, highlighting severe cross-border tracking gaps (PopCAB), detection/notification delays (7-1-7), and local administrative/surveillance friction (CDC Attributes).

Local Dialect: Written in authentic Chavacano-infused Tagalog/Taglish (common in the Southern Philippines/Zamboanga peninsula and Sulu archipelago border zones) to capture regional flavor.

Trascript Data: demo1.txt
Open the demo.txt and copy/paste the transcript in the "Transcript Analysis Workspace"

Target Framework 1: Hybrid (Deductive-Inductive) Approach
Target Framework 2: PopCAB (Mobility Pathways & Hubs; Point of Entry Gaps; Cross-border Health Info sharing)
Target Framework 3: 7-1-7 Framework (D1, R3, R6)

################################ RUN DEMO2 ###################################
SCENARIO: Avial Influenza Spill-over

This scenario represents a classic One Health intersection: a hypothetical outbreak of highly pathogenic avian influenza (H5N1) in a rural farming community. It has been written in realistic "Taglish" (Tagalog-English) to mirror how real-world field interviews sound in the Philippines.

Open the demo2.txt and copy/paste the transcript in the "Transcript Analysis Workspace"
Targeted Framework 1: One Health (Track 2 & 4)
Targeted Framework 2: CDC Surveillance System Attributes (Sensitivity and Acceptability)

## What will you see?

One Health Track 2 (Emerging Zoonotic Spillover): Maps to the quote about the dead ducks being dumped in the canal and the farmer disposing of them with bare hands. The Bottleneck Memo will highlight the failure to isolate the animal-human interface and the lack of joint safety protocols.

CDC Sensitivity & Acceptability Barriers: Maps to the farmers refusing to report for fear of culling/losing their livelihoods without compensation (Acceptability), and the RIGID digital system lacking options for animal exposures (Sensitivity/Flexibility).