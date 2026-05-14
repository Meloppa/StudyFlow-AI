import os
import markdown
from weasyprint import HTML
from google import genai
import io

# Setup the client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_writer(context_data):
    # Truncate context to keep it safe for the Free Tier
    safe_context = context_data[:8000] 
    
    prompt = f"""
    Create a professional Markdown Study Guide from this data:
    {safe_context}
    
    Include a TL;DR, an Action Plan, and a Resource Library.
    """
    
    try:
        # 1. Attempt with the standard stable model
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        md_text = response.text
    except Exception as e:
        print(f"⚠️ gemini-2.0-flash failed: {e}. Trying fallback...")
        try:
            # 2. NESTED TRY: Attempt with the lite model if the first one fails
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt
            )
            md_text = response.text
        except Exception as e2:
            # 3. FINAL FAILURE: If both models fail
            print(f"❌ BOTH MODELS FAILED: {str(e2)}")
            md_text = f"# Study Guide Error\n\nThe AI hit a limit: {str(e2)}\n\n**Tip:** Please wait 60 seconds and try again."

    # --- PDF CONVERSION ---
    html_content = markdown.markdown(md_text)
    styled_html = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 20mm; }}
            body {{ font-family: sans-serif; line-height: 1.6; color: #333; }}
            h1 {{ color: #1a73e8; }}
            h2 {{ color: #0d47a1; border-bottom: 1px solid #ddd; }}
        </style>
    </head>
    <body>{html_content}</body>
    </html>
    """
    
    try:
        pdf_bytes = HTML(string=styled_html).write_pdf()
    except Exception as pdf_err:
        print(f"❌ PDF ERROR: {pdf_err}")
        pdf_bytes = b"" 

    return md_text, pdf_bytes