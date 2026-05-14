import os
from google import genai
from google.genai import types

# Setup the client using environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_research(topic):
    print(f"\n🚀 StudyFlow Agent initiating research on: '{topic}'")
    
    # We use 2.0-flash because it's currently more stable than 3.1-lite
    stable_model = 'gemini-2.0-flash'
    
    try:
        # 1. Attempt Live Search Grounding
        response = client.models.generate_content(
            model=stable_model,
            contents=f"Perform a deep-dive research into: {topic}. Provide 3 reliable sources and a summary.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text

    except Exception as e:
        print(f"⚠️ Search tool failed or busy: {e}. Trying fallback strategy...")
        
        try:
            # 2. Fallback: Use internal knowledge if the Search Tool is down
            fallback = client.models.generate_content(
                model=stable_model,
                contents=f"I am unable to access the live web right now. Based on your topic '{topic}', suggest a research strategy, 3 key academic databases, and 3 specific search strings to use."
            )
            return fallback.text
        except Exception as e2:
            # 3. Final Error Catch
            return f"❌ Research Agent is currently unavailable. Error: {str(e2)}"

if __name__ == "__main__":
    # Test block
    print(studyflow_research("AI in supply chain 2026"))