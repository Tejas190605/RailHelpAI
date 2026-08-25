import os
import io
import uuid
import logging
from typing import Dict, Any
from PIL import Image

logger = logging.getLogger(__name__)

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
UPLOAD_DIR = "data/uploads"


def validate_and_save_image(file_bytes: bytes, original_filename: str) -> Dict[str, Any]:
    """
    Safely validate image bytes, verify MIME format, strip EXIF metadata, and save locally.
    Returns file metadata dictionary.
    """
    file_size = len(file_bytes)
    if file_size > MAX_FILE_SIZE_BYTES:
        return {
            "valid": False,
            "error": f"File size ({round(file_size / (1024*1024), 2)} MB) exceeds maximum 5.0 MB limit."
        }

    ext = os.path.splitext(original_filename.lower())[1]
    if ext not in ALLOWED_EXTENSIONS:
        return {
            "valid": False,
            "error": f"Invalid extension '{ext}'. Only .jpg, .jpeg, and .png images are permitted."
        }

    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.verify()
        
        # Re-open for clean processing & EXIF stripping
        image = Image.open(io.BytesIO(file_bytes))
        
        # Convert RGBA to RGB for JPEG compatibility
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Strip EXIF metadata by creating fresh image object
        data_clean = list(image.getdata())
        clean_img = Image.new(image.mode, image.size)
        clean_img.putdata(data_clean)

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        unique_name = f"img_{uuid.uuid4().hex[:12]}{ext}"
        save_path = os.path.join(UPLOAD_DIR, unique_name)
        
        clean_img.save(save_path)

        return {
            "valid": True,
            "file_path": save_path,
            "file_name": unique_name,
            "file_size_bytes": file_size,
            "mime_type": f"image/{ext.replace('.', '')}",
            "width": image.width,
            "height": image.height
        }
    except Exception as e:
        logger.error(f"Image validation failed: {e}")
        return {"valid": False, "error": f"Corrupted or unreadable image file: {str(e)}"}
