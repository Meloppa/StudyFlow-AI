import os
import time
from google import genai
from google.genai import types

# Setup the client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_research(topic):
    print(f"\n🚀 StudyFlow Research Agent initiating: '{topic}'")
    
    # Using the 2026 Speed King
    active_model = 'gemini-3.1-flash-lite'
    
    try:
        # 1. Attempt Live Search Grounding
        response = client.models.generate_content(
            model=active_model,
            contents=f"Perform deep-dive research into: {topic}. Provide 3 reliable sources and a summary.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text

    except Exception as e:
        error_msg = str(e)
        
        # Friendly handling for the Free Tier "Speed Ticket"
        if "429" in error_msg:
            print("⚠️ Rate limit hit. Guidance: Wait 60s.")
            return "⏳ **Search Limit Reached.** The Google Search tool is cooling down. Please wait about 60 seconds and click 'Run Research Agent' again to get your sources!"
            
        print(f"⚠️ Search tool error: {error_msg}. Trying fallback...")
        
        try:
            # 2. Fallback: Use Internal Knowledge if Search is down/busy
            fallback = client.models.generate_content(
                model=active_model,
                contents=f"I can't access live search right now. Based on your knowledge, suggest a research strategy for: {topic}."
            )
            return fallback.text
        except Exception as e2:
            return f"❌ Research Agent is currently unavailable: {str(e2)}"