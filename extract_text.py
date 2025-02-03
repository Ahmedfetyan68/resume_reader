import pdfplumber
import docx2txt

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF resume."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX resume."""
    return docx2txt.process(docx_path).strip()
