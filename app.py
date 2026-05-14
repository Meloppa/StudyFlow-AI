from google import genai
import streamlit as st
import ingestor
import researcher
import writer
import os

# Page Config
st.set_page_config(page_title="StudyFlow AI", page_icon="🌊", layout="centered")

st.title("🌊 StudyFlow AI")
st.subheader("Your Intelligent Academic Orchestrator")

# 1. File Upload Section
st.write("### 1. Upload Assignment")
uploaded_file = st.file_uploader("Choose a PDF or Image", type=['pdf', 'png', 'jpg', 'jpeg'])

if uploaded_file:
    # Save the file locally so the Ingestor can find it
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    if st.button("🔍 Analyze Document"):
        with st.spinner("Analyzing document with Gemini 3.1..."):
            # We call the function and display results
            analysis = ingestor.studyflow_ingest_auto() 
            st.session_state['analysis'] = analysis # Store in memory
            st.markdown("### 📋 Assignment Summary")
            st.write(analysis)

# 2. Research Section
if 'analysis' in st.session_state:
    st.write("---")
    st.write("### 2. Deep Dive Research")
    user_topic = st.text_input("What specific topic should I research for you?")
    
    if st.button("🚀 Run Research Agent"):
        with st.spinner("Searching the web..."):
            research_results = researcher.studyflow_research(user_topic)
            st.session_state['research'] = research_results
            st.markdown("### 🔎 Research Findings")
            st.write(research_results)

# 3. Final Output Section
if 'research' in st.session_state:
    st.write("---")
    st.write("### 3. Generate Final Study Guide")
    if st.button("✍️ Draft My Guide"):
        with st.spinner("Writing professional study guide..."):
            context = f"ANALYSIS: {st.session_state['analysis']}\nRESEARCH: {st.session_state['research']}"
            # Modify writer to return the text!
            final_guide = writer.studyflow_writer(context) 
            st.markdown(final_guide)
            
            # Download Button
            st.download_button(
                label="📥 Download Study Plan (.md)",
                data=final_guide,
                file_name="StudyPlan.md",
                mime="text/markdown"
            )