import os
import markdown
from weasyprint import HTML
from google import genai
import io

# Setup the client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_writer(context_data):
    # 1. TRUNCATE CONTEXT (Safety First)
    # If the context is massive, we take only the most important parts 
    # to avoid hitting Free Tier "Token" limits.
    safe_context = context_data[:10000] # Limits to roughly 2,500 words
    
    print(f"✍️ Agent is drafting guide... (Context size: {len(safe_context)} chars)")
    
    prompt = f"""
    Create a professional Markdown Study Guide based on this data:
    
    {safe_context}
    
    Include: TL;DR, Action Plan, and Resources. 
    Use clear headings and bold text.
    """
    
    try:
        # 2. USE 1.5-FLASH (The most stable workhorse for Free Tier)
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=prompt
        )
        md_text = response.text
        
    except Exception as e:
        # This will print the REAL error in your "Manage App" -> "Logs" in Streamlit
        print(f"❌ ERROR IN WRITER AGENT: {str(e)}")
        md_text = f"# Study Guide Error\n\nThe AI hit a limit: {str(e)}\n\n**Tip:** Try researching a smaller/more specific topic."

    # 3. CONVERT TO PDF
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
        pdf_bytes = b"" # Return empty bytes if PDF fails

    return md_text, pdf_bytes