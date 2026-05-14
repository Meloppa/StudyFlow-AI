import streamlit as st
import ingestor
import researcher
import writer
import os

# Page Config
st.set_page_config(page_title="StudyFlow AI", page_icon="🌊", layout="centered")

st.title("🌊 StudyFlow AI")
st.subheader("Your Intelligent Academic Orchestrator")

# --- 1. FILE UPLOAD SECTION ---
st.write("### 1. Upload Assignment")
uploaded_file = st.file_uploader("Choose a PDF or Image", type=['pdf', 'png', 'jpg', 'jpeg'])

if uploaded_file:
    # Save locally for the Ingestor agent to find it
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("🔍 Analyze Document"):
        with st.spinner("Analyzing document with Gemini 3.1..."):
            analysis = ingestor.studyflow_ingest_auto() 
            st.session_state['analysis'] = analysis 

# Persistent display of Analysis
if 'analysis' in st.session_state:
    st.info("✅ Document Analyzed")
    with st.expander("See Assignment Summary", expanded=True):
        st.markdown(st.session_state['analysis'])

# --- 2. RESEARCH SECTION ---
if 'analysis' in st.session_state:
    st.write("---")
    st.write("### 2. Deep Dive Research")
    user_topic = st.text_input("What specific topic should I research for you?", placeholder="e.g., Sustainable supply chain trends 2026")
    
    if st.button("🚀 Run Research Agent"):
        with st.spinner("Searching the web..."):
            research_results = researcher.studyflow_research(user_topic)
            st.session_state['research'] = research_results

# Persistent display of Research
if 'research' in st.session_state:
    st.info("✅ Research Complete")
    with st.expander("See Research Findings", expanded=True):
        st.markdown(st.session_state['research'])

# --- 3. FINAL OUTPUT SECTION ---
if 'research' in st.session_state:
    st.write("---")
    st.write("### 3. Generate Final Study Guide")
    
    if st.button("✍️ Draft My Guide"):
        with st.spinner("Writing and converting to PDF..."):
            # Only take the first 4000 characters of each to stay under the TPM limit
            short_analysis = st.session_state['analysis'][:4000]
            short_research = st.session_state['research'][:4000]
            
            context = f"ASSIGNMENT SUMMARY: {short_analysis}\n\nRESEARCH DATA: {short_research}"
            
            # Pass the trimmed context
            final_text, final_pdf_bytes = writer.studyflow_writer(context)
            
            st.session_state['final_text'] = final_text
            st.session_state['pdf_bytes'] = final_pdf_bytes

    # Persistent display of Final Guide & Download
    if 'final_text' in st.session_state:
        st.success("✨ Your Study Guide is Ready!")
        st.markdown(st.session_state['final_text'])
        
        st.download_button(
            label="📥 Download Study Plan (PDF)",
            data=st.session_state['pdf_bytes'],
            file_name="StudyPlan.pdf",
            mime="application/pdf"
        )