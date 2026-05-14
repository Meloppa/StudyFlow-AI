import streamlit as st
import ingestor
import writer
import os

# 1. PAGE CONFIG & MODERN STYLING
st.set_page_config(page_title="StudyFlow AI", page_icon="🌊", layout="centered")

# Custom CSS for a professional "SaaS" look
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .title-text {
        font-family: 'Inter', sans-serif;
        color: #1E3A8A;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    div.stButton > button {
        background-color: #1a73e8;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 0.5rem;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0d47a1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stExpander {
        background: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='title-text'>🌊 StudyFlow AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563;'>Your Intelligent Academic Orchestrator</p>", unsafe_allow_html=True)
st.write("---")

# --- 1. FILE UPLOAD SECTION ---
st.write("### 📄 1. Upload Assignment")
uploaded_file = st.file_uploader("Choose a PDF or Image", type=['pdf', 'png', 'jpg', 'jpeg'])

if uploaded_file:
    # Save locally for the Ingestor agent
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("🔍 Analyze Document"):
        with st.spinner("Analyzing document with Gemini 3.1..."):
            analysis_results = ingestor.studyflow_ingest_auto() 
            st.session_state['analysis'] = analysis_results

# Persistent display of Analysis
if 'analysis' in st.session_state:
    st.success("✅ Document Analyzed")
    with st.expander("See Assignment Summary", expanded=True):
        st.markdown(st.session_state['analysis'])

    # --- 2. FINAL OUTPUT SECTION (Directly after Analysis) ---
    st.write("---")
    st.write("### ✍️ 2. Generate Final Study Guide")
    
    if st.button("🪄 Draft My Guide"):
        with st.spinner("Writing and converting to PDF..."):
            # Use the analysis results as the sole context
            context = f"ASSIGNMENT SUMMARY: {st.session_state['analysis'][:8000]}"
            
            final_text, final_pdf_bytes = writer.studyflow_writer(context)
            
            st.session_state['final_text'] = final_text
            st.session_state['pdf_bytes'] = final_pdf_bytes

    # Persistent display of Final Guide & Download
    if 'final_text' in st.session_state:
        st.markdown("---")
        st.subheader("✨ Your Personalized Study Guide")
        st.markdown(st.session_state['final_text'])
        
        st.download_button(
            label="📥 Download Study Plan (PDF)",
            data=st.session_state['pdf_bytes'],
            file_name="StudyPlan.pdf",
            mime="application/pdf"
        )