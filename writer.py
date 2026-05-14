import os
import markdown
from weasyprint import HTML
from google import genai
import io
import time

# Setup the client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_writer(context_data):
    # Truncate context to keep it safe for the Free Tier (approx 2.5k words)
    safe_context = context_data[:10000] 
    
    prompt = f"""
    Create a professional Markdown Study Guide from this data:
    {safe_context}
    
    Include a TL;DR, an Action Plan, and a Resource Library. Make it specific and detailed. 
    """
    
    # 3.1-flash-lite is the 2026 "Speed King" for Free Tier
    active_model = 'gemini-3.1-flash-lite'
    
    try:
        response = client.models.generate_content(
            model=active_model, 
            contents=prompt
        )
        md_text = response.text
    except Exception as e:
        if "429" in str(e):
            print("Rate limit hit. Waiting 10 seconds for 3.1 quota reset...")
            time.sleep(10)
            try:
                # Retry once more with the same model
                response = client.models.generate_content(
                    model=active_model, 
                    contents=prompt
                )
                md_text = response.text
            except:
                md_text = "❌ Quota exceeded on 3.1 Flash-Lite. Please wait 60 seconds."
        else:
            md_text = f"❌ Error: {str(e)}"

    # --- PDF CONVERSION ---
    html_content = markdown.markdown(md_text)
    styled_html = f"<html><body>{html_content}</body></html>"
    
    try:
        pdf_bytes = HTML(string=styled_html).write_pdf()
    except:
        pdf_bytes = b"" 

    return md_text, pdf_bytes