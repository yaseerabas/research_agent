import fitz  # PyMuPDF
from docx import Document
from fpdf import FPDF
import tempfile
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def save_report_as_pdf(content):
    from fpdf import FPDF
    import tempfile

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Get the absolute path to the font file
    base_path = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_path, "DejaVuSans.ttf")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    return temp_pdf.name

def save_report_as_docx(content):
    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)

    temp_docx = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp_docx.name)
    return temp_docx.name

