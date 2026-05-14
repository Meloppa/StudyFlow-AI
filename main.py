import ingestor
import researcher
import writer
from google import genai
import os

# Use your working key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def run_studyflow_system():
    print("\n" + "="*40)
    print("🌊 WELCOME TO STUDYFLOW AI v3.1 🌊")
    print("="*40)

    # 1. STEP ONE: INGESTION
    file_to_process = ingestor.get_latest_assignment()
    
    if not file_to_process:
        print("❌ No files found in folder.")
        return

    print(f"📄 Analyzing: {file_to_process}...")
    
    # We modify the call to capture the summary text
    # (Note: For this to work perfectly, ensure your ingestor.py returns the response.text)
    ingest_summary = ingestor.studyflow_ingest_auto() 

    print("\n" + "-"*30)
    print("🤖 INGESTION COMPLETE.")
    print("-"*30)

    # 2. STEP TWO: RESEARCH
    print("\nWhat specific part should I research for you?")
    user_topic = input("Enter research topic (or press Enter to skip): ")

    research_data = ""
    if user_topic.strip():
        # Captures the research results
        research_data = researcher.studyflow_research(user_topic)
    else:
        print("⏩ Skipping research phase.")

    # 3. STEP THREE: THE WRITER (The Final Polish)
    print("\n✨ Connecting all agents to draft your final guide...")
    
    # We combine the findings into one big "Context" for the writer
    master_context = f"""
    ASSIGNMENT SUMMARY:
    {ingest_summary}
    
    USER RESEARCH REQUESTED: {user_topic}
    RESEARCH FINDINGS:
    {research_data}
    """
    
    writer.studyflow_writer(master_context)

    print("\n" + "="*40)
    print("🏁 PROCESS COMPLETE: Check 'StudyPlan.md'!")
    print("="*40)

if __name__ == "__main__":
    run_studyflow_system()