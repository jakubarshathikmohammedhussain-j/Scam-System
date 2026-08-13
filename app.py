import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json
import io
from gtts import gTTS

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & GLOBAL SETUP
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="S.C.A.M. SYSTEM - HOLO EARTH",
    page_icon="👁️‍🗨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CORPORATE ANIME & VFX THEME (CSS INJECTION)
# -----------------------------------------------------------------------------
cyberpunk_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@400;500;700&display=swap');

    /* Base App Styling */
    .stApp {
        background-color: #050814;
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
        background-image: 
            linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* Headings & Text */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .glow-header {
        color: #00f3ff;
        text-shadow: 0 0 5px rgba(0, 243, 255, 0.5), 0 0 10px rgba(0, 243, 255, 0.3);
        animation: neon-pulse-cyan 2s infinite alternate;
    }

    .glow-subheader {
        color: #ffaa00;
        text-shadow: 0 0 5px rgba(255, 170, 0, 0.8), 0 0 10px rgba(255, 170, 0, 0.5);
        animation: neon-pulse-amber 3s infinite alternate;
        font-weight: 700;
    }

    /* Animations */
    @keyframes neon-pulse-cyan {
        0% { text-shadow: 0 0 5px #00f3ff, 0 0 10px #00f3ff; }
        100% { text-shadow: 0 0 10px #00f3ff, 0 0 25px #00f3ff, 0 0 40px #00f3ff; }
    }
    
    @keyframes neon-pulse-amber {
        0% { text-shadow: 0 0 5px #ffaa00; }
        100% { text-shadow: 0 0 10px #ffaa00, 0 0 20px #ffaa00; }
    }

    @keyframes fade-in-up {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Input & UI Elements */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(5, 8, 20, 0.8) !important;
        color: #00f3ff !important;
        border: 1px solid #00f3ff !important;
        border-radius: 0px !important;
        font-family: 'Rajdhani', monospace !important;
        box-shadow: inset 0 0 10px rgba(0, 243, 255, 0.1);
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #ffaa00 !important;
        box-shadow: 0 0 10px rgba(255, 170, 0, 0.5), inset 0 0 10px rgba(255, 170, 0, 0.2) !important;
    }

    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #050814, #0a1128);
        color: #00f3ff;
        border: 1px solid #00f3ff;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        border-radius: 0px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.2);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: rgba(0, 243, 255, 0.1);
        color: #ffaa00;
        border: 1px solid #ffaa00;
        box-shadow: 0 0 20px rgba(255, 170, 0, 0.6);
        transform: scale(1.02);
    }

    /* Download Buttons Special Styling */
    .stDownloadButton > button {
        background: rgba(255, 170, 0, 0.05);
        color: #ffaa00;
        border-color: #ffaa00;
    }
    .stDownloadButton > button:hover {
        background: rgba(255, 170, 0, 0.2);
        color: #00f3ff;
        border-color: #00f3ff;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.6);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 2px solid rgba(0, 243, 255, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', sans-serif;
        color: rgba(255, 255, 255, 0.5);
    }
    .stTabs [aria-selected="true"] {
        color: #00f3ff !important;
        border-bottom: 2px solid #00f3ff !important;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #03050c !important;
        border-right: 1px solid rgba(0, 243, 255, 0.2);
        box-shadow: 5px 0 15px rgba(0, 0, 0, 0.8);
    }

    /* Metric & Summary Cards */
    .neon-metric-card {
        background: rgba(5, 8, 20, 0.9);
        border-left: 4px solid #ffaa00;
        border-right: 4px solid #ffaa00;
        padding: 20px;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        color: #ffaa00;
        text-shadow: 0 0 15px rgba(255, 170, 0, 0.6);
        box-shadow: inset 0 0 20px rgba(255, 170, 0, 0.1), 0 0 15px rgba(0, 0, 0, 0.8);
        margin-bottom: 20px;
    }
    
    .cio-summary-box {
        background: rgba(0, 243, 255, 0.05);
        border: 1px solid rgba(0, 243, 255, 0.3);
        border-left: 5px solid #00f3ff;
        padding: 25px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        color: #e0e0e0;
        line-height: 1.6;
        box-shadow: inset 0 0 15px rgba(0, 243, 255, 0.05);
        margin-top: 20px;
    }

    .cio-summary-box strong {
        color: #ffaa00;
        font-family: 'Orbitron', sans-serif;
    }
</style>
"""
st.markdown(cyberpunk_css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def generate_gtts_audio(text_content):
    """Generates TTS audio strictly in memory using io.BytesIO."""
    tts = gTTS(text=text_content, lang='en', tld='co.uk', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# Initialize Session State
if "api_initialized" not in st.session_state:
    st.session_state.api_initialized = False
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "scam_analysis" not in st.session_state:
    st.session_state.scam_analysis = None

# -----------------------------------------------------------------------------
# SIDEBAR: API AUTH NODE
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 class='glow-header' style='text-align: center;'>API AUTH NODE</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #00f3ff; opacity: 0.3;'>", unsafe_allow_html=True)
    
    key_input = st.text_input("ENTER SYSTEM KEY (GEMINI API)", type="password")
    
    if st.button("INITIALIZE SYSTEM"):
        if key_input.strip() != "":
            st.session_state.api_key = key_input.strip()
            st.session_state.api_initialized = True
            st.success("🟢 SYSTEM LINK ESTABLISHED.")
        else:
            st.error("🔴 OVERRIDE DENIED: KEY REQUIRED.")

    st.markdown("<div style='margin-top: 50px; font-family: Rajdhani; font-size: 0.9em; color: gray;'>STATUS: " + 
                ("<span style='color: #00ff66;'>ONLINE</span>" if st.session_state.api_initialized else "<span style='color: #ff003c;'>OFFLINE</span>") + 
                "</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN LAYOUT & NAVIGATION
# -----------------------------------------------------------------------------
tab1, tab2 = st.tabs(["⚙️ CONTROL NODE", "📊 HOLO-ANALYTICS"])

# =============================================================================
# TAB 1: CONTROL NODE
# =============================================================================
with tab1:
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.markdown("<h1 class='glow-header' style='text-align: center; font-size: 4em; margin-bottom: 0px;'>S.C.A.M. SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='glow-subheader' style='text-align: center; margin-top: 0px;'>MADE BY HOLO EARTH</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='color: #00f3ff;'>[ DATA INGESTION MATRIX ]</h4>", unsafe_allow_html=True)
        uploaded_csv = st.file_uploader("UPLOAD DATA CORE (CSV)", type=["csv"])
    
    with col2:
        st.markdown("<h4 style='color: #00f3ff;'>[ MANUAL OVERRIDE INJECTION ]</h4>", unsafe_allow_html=True)
        raw_text_input = st.text_area("INJECT RAW TEXT DATA", height=120, placeholder="Paste raw software inventory logs here...")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("EXECUTE PURGE"):
        if not st.session_state.api_initialized:
            st.error("⚠️ SYSTEM OFFLINE. INITIALIZE API AUTH NODE FIRST.")
        elif not uploaded_csv and not raw_text_input.strip():
            st.warning("⚠️ INSUFFICIENT DATA. UPLOAD CSV OR INJECT TEXT.")
        else:
            with st.spinner("INITIATING NEURAL ANALYSIS..."):
                try:
                    # Semantic Clustering Logic Setup
                    input_context = ""
                    if uploaded_csv:
                        df_upload = pd.read_csv(uploaded_csv)
                        input_context = df_upload.head(50).to_csv(index=False)
                    else:
                        input_context = raw_text_input

                    # Configure Definitive Generative AI SDK
                    genai.configure(api_key=st.session_state.api_key)
                    model = genai.GenerativeModel("gemini-3.5 flash lite")
                    
                    # Construct Prompt
                    system_prompt = f"""
                    You are a cynical, hyper-analytical Corporate CIO detecting software redundancy.
                    Analyze the following software inventory data. Identify overlapping tools, wasted spend, and consolidation opportunities.
                    
                    CRITICAL INSTRUCTION: You must respond STRICTLY with a valid JSON object matching the exact schema below. Do not include markdown formatting, backticks, or conversational text.
                    
                    JSON SCHEMA:
                    {{
                        "total_wasted_spend": float,
                        "optimized_budget": float,
                        "redundant_clusters": [
                            {{
                                "category": string,
                                "overlapping_tools": [string, string, ...],
                                "total_category_waste": float,
                                "mitigation_plan": string
                            }}
                        ],
                        "cio_briefing": string
                    }}
                    
                    DATA PAYLOAD:
                    {input_context}
                    """

                    # Call Gemini API with Structured Output Mandate
                    response = model.generate_content(
                        system_prompt,
                        generation_config={"response_mime_type": "application/json"}
                    )
                    
                    # Parse and Store Response
                    result_json = json.loads(response.text)
                    st.session_state.scam_analysis = result_json
                    
                    st.success("🟢 PURGE ANALYSIS COMPLETE.")

                except Exception as e:
                    st.error(f"⚠️ SYSTEM FAULT DETECTED: {str(e)}")

    # Display Results & Audio if Analysis Exists
    if st.session_state.scam_analysis:
        st.markdown("<hr style='border-color: #ffaa00; opacity: 0.5;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #ffaa00;'>[ EXECUTIVE CIO BRIEFING ]</h4>", unsafe_allow_html=True)
        
        briefing_text = st.session_state.scam_analysis.get('cio_briefing', 'No briefing provided.')
        
        # UI Container for Summary
        st.markdown(f"""
        <div class='cio-summary-box'>
            <strong>DIRECTIVE:</strong> {briefing_text}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><p style='color: #00f3ff; font-family: Rajdhani; font-weight: bold;'>[ AUTO-PLAYBACK NEURAL SYNTHESIS ]</p>", unsafe_allow_html=True)
        # Dynamic Voice Synthesis (In-memory)
        audio_stream = generate_gtts_audio(briefing_text)
        st.audio(audio_stream, format="audio/mp3")
        
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 2: HOLO-ANALYTICS
# =============================================================================
with tab2:
    if st.session_state.scam_analysis is None:
        st.info("AWAITING DATA PURGE EXECUTION IN CONTROL NODE.")
    else:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        
        data = st.session_state.scam_analysis
        total_waste = data.get('total_wasted_spend', 0.0)
        
        # 1. Custom HTML Neon Metric Card
        st.markdown(f"""
        <div class='neon-metric-card'>
            TOTAL WASTED SPEND DETECTED<br>
            <span style='color: #00f3ff;'>${total_waste:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

        # Process data for Plotly and Dataframe
        clusters = data.get('redundant_clusters', [])
        flattened_data = []
        for cluster in clusters:
            cat = cluster.get('category', 'Unknown')
            tools = cluster.get('overlapping_tools', [])
            cat_waste = cluster.get('total_category_waste', 0.0)
            mitigation = cluster.get('mitigation_plan', 'None')
            
            # Distribute waste visually across tools for the treemap
            tool_waste_val = cat_waste / len(tools) if len(tools) > 0 else 0
            
            for tool in tools:
                flattened_data.append({
                    "Sector / Category": cat,
                    "Identified Tool": tool,
                    "Estimated Waste ($)": round(tool_waste_val, 2),
                    "Mitigation Strategy": mitigation
                })
        
        df_clusters = pd.DataFrame(flattened_data)

        colA, colB = st.columns([2, 1])
        
        with colA:
            # 2. Plotly px.treemap (Software Sprawl Topography)
            st.markdown("<h4 style='color: #00f3ff;'>[ SOFTWARE SPRAWL TOPOGRAPHY ]</h4>", unsafe_allow_html=True)
            if not df_clusters.empty:
                # Add a root node for treemap scaling
                df_clusters["Root"] = "ENTERPRISE STACK"
                fig = px.treemap(
                    df_clusters, 
                    path=["Root", "Sector / Category", "Identified Tool"], 
                    values="Estimated Waste ($)",
                    color="Sector / Category",
                    color_discrete_sequence=['#00f3ff', '#ffaa00', '#ff0055', '#a200ff', '#00ffaa']
                )
                
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Orbitron", color="#e0e0e0"),
                    margin=dict(t=20, l=10, r=10, b=10)
                )
                
                fig.data[0].textinfo = 'label+value+percent parent'
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No redundant cluster data available to map.")

        with colB:
            # Voice Diagnostic Trigger
            st.markdown("<h4 style='color: #ffaa00;'>[ EXECUTIVE COMMAND ]</h4>", unsafe_allow_html=True)
            if st.button("🎙️ AUDIO DIAGNOSTIC"):
                top_category = df_clusters['Sector / Category'].iloc[0] if not df_clusters.empty else "various sectors"
                diagnostic_text = f"System alert. Estimated total wasted spend is {int(total_waste)} dollars. Severe redundancy detected primarily in the {top_category} sector. Execute consolidation protocols immediately."
                
                diag_audio = generate_gtts_audio(diagnostic_text)
                st.audio(diag_audio, format="audio/mp3")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Export Controls
            st.markdown("<h4 style='color: #00f3ff;'>[ DATA EXPORT NODES ]</h4>", unsafe_allow_html=True)
            if not df_clusters.empty:
                csv_export = df_clusters.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="DOWNLOAD LEDGER (CSV)",
                    data=csv_export,
                    file_name="scam_redundancy_ledger.csv",
                    mime="text/csv",
                )
                
                html_export = fig.to_html(include_plotlyjs="cdn")
                st.download_button(
                    label="DOWNLOAD TOPOGRAPHY (HTML)",
                    data=html_export,
                    file_name="scam_topography.html",
                    mime="text/html"
                )

        # 3. Interactive st.dataframe Ledger
        st.markdown("<h4 style='color: #00f3ff; margin-top: 30px;'>[ RAW DATA LEDGER ]</h4>", unsafe_allow_html=True)
        st.dataframe(
            df_clusters, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Estimated Waste ($)": st.column_config.NumberColumn(format="$%.2f")
            }
        )

        st.markdown("</div>", unsafe_allow_html=True)
  
