import os
import markdown
from weasyprint import HTML
from google import genai
import io

# Setup the client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_writer(context_data):
    print("\n✍️ Agent is drafting your Final Study Guide...")
    
    prompt = f"""
    You are the StudyFlow Content Creator. 
    Create a beautifully formatted Markdown Study Guide from this data:
    
    {context_data}
    
    Include a TL;DR, an Action Plan, and a Resource Library.
    Use professional university-level tone.
    """
    
    try:
        # SWITCHED MODEL TO 2.0-FLASH FOR STABILITY
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        md_text = response.text
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        md_text = "# Study Guide\n\nError generating full content. Please try again in a moment."

    # 1. Convert Markdown to HTML for the PDF
    html_content = markdown.markdown(md_text)
    
    styled_html = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 20mm; }}
            body {{ font-family: 'Helvetica', sans-serif; line-height: 1.6; color: #333; }}
            h1 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; }}
            h2 {{ color: #0d47a1; margin-top: 15px; }}
            li {{ margin-bottom: 8px; }}
        </style>
    </head>
    <body>{html_content}</body>
    </html>
    """
    
    # 2. Generate PDF bytes
    try:
        pdf_bytes = HTML(string=styled_html).write_pdf()
    except Exception as e:
        print(f"PDF Conversion Error: {e}")
        pdf_bytes = b"" # Empty bytes if PDF fails

    return md_text, pdf_bytes