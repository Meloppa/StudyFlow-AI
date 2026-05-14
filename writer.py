import os
import markdown
from weasyprint import HTML
from google import genai
import io

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def studyflow_writer(context_data):
    print("\n✍️ Drafting your Final PDF Study Guide...")
    
    prompt = f"""
    You are the StudyFlow Content Creator. 
    Create a beautifully formatted Study Guide from this data: {context_data}
    Use Heading 1 for the title, Heading 2 for sections, and bullet points.
    """
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    
    md_text = response.text
    
    # 1. Convert Markdown to HTML
    html_content = markdown.markdown(md_text)
    styled_html = f"<html><body>{html_content}</body></html>" # simplified for example
    
    # 2. Add some professional CSS Styling
    styled_html = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 20mm; }}
            body {{ font-family: 'Helvetica', sans-serif; line-height: 1.6; color: #333; }}
            h1 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; }}
            h2 {{ color: #0d47a1; margin-top: 20px; }}
            li {{ margin-bottom: 10px; }}
        </style>
    </head>
    <body>{html_content}</body>
    </html>
    """
    
    # 3. Save as PDF
    pdf_bytes = HTML(string=styled_html).write_pdf()
    
    print("✅ PDF generated: StudyPlan.pdf")
    return md_text, pdf_bytes # Still return text so the UI can display it too

if __name__ == "__main__":
    studyflow_writer("Test data for PDF generation.")