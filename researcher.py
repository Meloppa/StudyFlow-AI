from google import genai
from google.genai import types
import os

# Setup the client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_research(topic):
    print(f"\n🚀 StudyFlow Agent initiating research on: '{topic}'")
    
    try:
        # Try Live Search
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=f"Perform a deep-dive research into: {topic}. Give me 3 sources and a summary.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        # We return the text so Streamlit can display it
        return response.text

    except Exception as e:
        # Fallback if quota is hit
        print(f"\n⚠️ Note: Live search tool restricted ({e}). Using internal knowledge base...")
        fallback = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=f"Suggest a research strategy and key academic sources for: {topic}"
        )
        # Return the fallback text to the UI
        return fallback.text

if __name__ == "__main__":
    # This part only runs if you play THIS file directly
    print("🎓 Welcome to the StudyFlow Research Terminal")
    print("-------------------------------------------")
    
    user_query = input("What topic do you want to research today? > ")
    
    if user_query.strip():
        # Capture the returned text and print it
        result = studyflow_research(user_query)
        print("\n--- RESULTS ---")
        print(result)
    else:
        print("❌ You didn't enter a topic.")