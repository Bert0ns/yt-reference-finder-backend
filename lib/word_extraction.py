import PyPDF2
import io
import pytesseract
from PIL import Image
from docx import Document
from lib.app_logger import logger
from werkzeug.datastructures import FileStorage


def _read_text_input(text_input) -> str:
    if hasattr(text_input, "read"):
        try:
            text_input.seek(0)
        except Exception:
            pass
        raw = text_input.read()
        if isinstance(raw, bytes):
            return raw.decode("utf-8", errors="replace")
        return str(raw)

    with open(text_input, "r", encoding="utf-8") as f:
        return f.read()


def extract_text_from_txt(txt_file):
    return _read_text_input(txt_file)


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_image(image_file):
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img, lang="ita")
    except Exception as e:
        logger.error(f"Error extracting text from image: {e}")
        text = ""

    return text


def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)


def extract_text_from_doc(doc_file):
    return extract_text_from_docx(doc_file)


def extract_text_from_md(md_file):
    return _read_text_input(md_file)


def read_file(file: FileStorage):
    success = True
    filename = file.filename
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".txt"):
        text = extract_text_from_txt(file)
    elif filename.endswith(".md"):
        text = extract_text_from_md(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    elif filename.endswith(".doc"):
        text = extract_text_from_doc(file)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        text = extract_text_from_image(file)
    else:
        text = ""
        success = False
        logger.warning(f"Unsupported file format or could not read file: {filename}")

    return success, text


def read_file_from_bytes(file_bytes: bytes, filename: str) -> tuple[bool, str]:
    text_content = ""
    # Create a file-like object from bytes
    file_like_object = io.BytesIO(file_bytes)

    try:
        if filename.endswith(".pdf"):
            text_content = extract_text_from_pdf(file_like_object)
        elif filename.endswith(".txt"):
            text_content = extract_text_from_txt(file_like_object)
        elif filename.endswith(".md"):
            text_content = extract_text_from_md(file_like_object)
        elif filename.endswith(".docx"):
            text_content = extract_text_from_docx(file_like_object)
        elif filename.endswith(".doc"):
            text_content = extract_text_from_doc(file_like_object)
        elif filename.endswith((".jpg", ".jpeg", ".png")):
            text_content = extract_text_from_image(file_like_object)
        else:
            logger.warning(f"Unsupported file format: {filename}")
            return False, ""  # Unsupported format

        # Ensure text_content is a string; some extractors may return None on failure
        if text_content is None:
            text_content = ""
            # If an extractor returns None, treat it as empty output for now

        return True, str(text_content)  # Ensure it is a string

    except Exception as e:
        logger.error(
            f"Error extracting text from file {filename} (type: {filename.split('.')[-1]}): {e}",
            exc_info=True,
        )
        return False, ""  # Extraction failed
