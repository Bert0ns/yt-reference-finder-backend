import PyPDF2
import pytesseract
from PIL import Image


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_image(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img, lang='ita')
    return text