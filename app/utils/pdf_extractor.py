import io
import os
from typing import Optional
from pypdf import PdfReader
from app.core.exceptions import FileProcessingException
from app.core.logging import logger


def extract_text_from_pdf_bytes(file_bytes: bytes, file_name: str = "uploaded_file.pdf") -> str:
    """
    Extracts plain text from raw PDF bytes using pypdf and pdfplumber fallbacks.
    """
    if not file_bytes:
        raise FileProcessingException(f"The PDF file '{file_name}' is empty.")

    extracted_text = ""
    # Try pypdf first
    try:
        pdf_stream = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)
        text_chunks = []
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
        extracted_text = "\n\n".join(text_chunks).strip()
    except Exception as e:
        logger.warning(f"pypdf extraction failed for '{file_name}': {e}. Trying pdfplumber...")

    # Fallback to pdfplumber if pypdf extracted nothing or failed
    if not extracted_text:
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                pages_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
                extracted_text = "\n\n".join(pages_text).strip()
        except Exception as e:
            logger.error(f"pdfplumber extraction also failed for '{file_name}': {e}")

    if not extracted_text or len(extracted_text.strip()) < 10:
        raise FileProcessingException(
            f"Could not extract readable text from '{file_name}'. The file may be image-only, scanned, or corrupted."
        )

    # Clean and normalize text
    normalized_text = clean_extracted_text(extracted_text)
    return normalized_text


def extract_text_from_pdf_file(file_path: str) -> str:
    """
    Reads a local PDF file and extracts its text content.
    """
    if not os.path.exists(file_path):
        raise FileProcessingException(f"PDF file path does not exist: {file_path}")

    try:
        with open(file_path, "rb") as f:
            content = f.read()
            return extract_text_from_pdf_bytes(content, os.path.basename(file_path))
    except Exception as e:
        logger.error(f"Error reading file '{file_path}': {e}")
        raise FileProcessingException(f"Failed to read file from disk: {str(e)}")


def clean_extracted_text(text: str) -> str:
    """
    Removes invalid characters, extra blank lines, and normalizes whitespaces.
    """
    if not text:
        return ""
    lines = [line.strip() for line in text.splitlines()]
    # Remove excessive blank lines
    non_empty_lines = []
    prev_empty = False
    for line in lines:
        if line:
            non_empty_lines.append(line)
            prev_empty = False
        elif not prev_empty:
            non_empty_lines.append("")
            prev_empty = True
    return "\n".join(non_empty_lines).strip()
