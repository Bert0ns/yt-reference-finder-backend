import PyPDF2
import pytesseract
from PIL import Image
from docx import Document
from lib.app_logger import logger


def extract_text_from_txt(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_image(image_file):
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img, lang='ita')
    except Exception as e:
        logger.error(f"Error extracting text from image: {e}")
        text = ""

    return text

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

def extract_text_from_doc(doc_file):
    return extract_text_from_docx(doc_file)

def extract_text_from_md(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()
    return text