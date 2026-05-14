import os
import glob
from google import genai
from google.genai import types

# 1. Setup the client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_latest_assignment():
    """Automatically finds the newest PDF or Image in the current folder."""
    valid_extensions = ("*.pdf", "*.png", "*.jpg", "*.jpeg")
    files = []
    for ext in valid_extensions:
        files.extend(glob.glob(ext))
    
    if not files:
        return None
        
    latest_file = max(files, key=os.path.getctime)
    return latest_file

def studyflow_ingest_auto():
    file_path = get_latest_assignment()
    
    if not file_path:
        return "❌ No assignment files found! Please add a PDF or Image to this folder."

    # These prints still show up in your black terminal (good for debugging)
    print(f"✅ Found newest file: {file_path}")
    print(f"--- Uploading to Gemini 3.1 ---")
    
    uploaded_file = client.files.upload(file=file_path)
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite', 
        contents=[
            uploaded_file,
            "Identify this document and provide a high-level summary of the requirements."
        ],
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(include_thoughts=True) 
        )
    )

    # THIS IS THE CHANGE:
    # Instead of just printing, we RETURN the text so the UI can catch it.
    return response.text

if __name__ == "__main__":
    # If running this file alone, we print it so we can see it
    result = studyflow_ingest_auto()
    print(result)