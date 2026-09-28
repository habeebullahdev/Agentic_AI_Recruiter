import json
import os
import re
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from app.core.config import settings
from app.core.exceptions import FileProcessingException, AIProcessingException
from app.core.logging import logger


def save_upload_file(file_bytes: bytes, original_filename: str) -> str:
    """
    Saves an uploaded file to the configured UPLOAD_DIR with a collision-resistant filename.
    Returns the absolute or relative saved file path.
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    extension = original_filename.split(".")[-1].lower() if "." in original_filename else "pdf"

    if extension not in settings.ALLOWED_EXTENSIONS:
        raise FileProcessingException(f"Invalid file format: '{extension}'. Allowed: {settings.ALLOWED_EXTENSIONS}")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    sanitized_name = re.sub(r'[^a-zA-Z0-9_\-.]', '_', original_filename)
    safe_filename = f"{timestamp}_{unique_id}_{sanitized_name}"
    target_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    try:
        with open(target_path, "wb") as buffer:
            buffer.write(file_bytes)
        return target_path
    except Exception as e:
        logger.error(f"Failed to write file to disk '{target_path}': {e}")
        raise FileProcessingException(f"Failed to save file: {str(e)}")


def parse_llm_json_response(raw_text: str) -> Dict[str, Any]:
    """
    Extracts and parses JSON object from LLM response, stripping markdown backticks if present.
    """
    if not raw_text:
        raise AIProcessingException("LLM returned an empty response")

    cleaned = raw_text.strip()

    # Strip markdown code blocks ```json ... ``` or ``` ... ```
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    # Attempt direct JSON parsing
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try regex search for first { ... } block
        match = re.search(r'(\{.*\})', cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError as err:
                logger.error(f"Failed regex-extracted JSON parse: {err}. Raw text:\n{cleaned}")
                raise AIProcessingException(f"Could not parse valid JSON from AI Agent response: {str(err)}")

        logger.error(f"Failed to parse LLM response into JSON. Raw:\n{raw_text}")
        raise AIProcessingException("AI Agent produced invalid JSON output structure")
