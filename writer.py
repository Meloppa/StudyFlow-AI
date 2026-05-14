from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_writer(context_data):
    print("\n✍️ Agent is drafting your Final Study Guide...")
    
    prompt = f"""
    You are the StudyFlow Content Creator. 
    Take the following raw data from our research and ingestion phase:
    
    {context_data}
    
    Create a beautifully formatted Markdown Study Guide. Include:
    1. A 'TL;DR' Executive Summary.
    2. A structured 'Action Plan' with checkboxes.
    3. A 'Resource Library' section with the research links provided.
    
    Use a professional, encouraging tone for a university student.
    """
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    
    # Save it to a file as a physical backup
    with open("StudyPlan.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("\n✅ Process Complete. Study Guide generated.")
    
    # IMPORTANT: Return the text so the UI can show it!
    return response.text

if __name__ == "__main__":
    # Instead of dummy data, we'll let you type a quick summary to test it
    print("🎓 StudyFlow Writer Test Mode")
    user_input = input("Enter some raw notes to turn into a guide: ")
    
    if user_input.strip():
        result = studyflow_writer(user_input)
        print("\n--- GENERATED GUIDE ---")
        print(result)