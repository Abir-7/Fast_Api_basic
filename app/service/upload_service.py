# app/services/upload_service.py
import shutil
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.utils.file_utils import detect_file_type

UPLOAD_DIR = Path("uploads")  # base folder for all files

class UploadService:

    @staticmethod
    async def save_file(file: UploadFile) -> dict: # type: ignore
        """
        Save an uploaded file to disk under uploads/<type>/uuid.ext
        Returns: dict with filename, type, and path
        """
        file_type = detect_file_type(file.filename) # type: ignore

        target_dir = UPLOAD_DIR / file_type
        target_dir.mkdir(parents=True, exist_ok=True)

        new_filename = f"{uuid4()}{Path(file.filename).suffix}" # type: ignore
        file_path = target_dir / new_filename

        # Save file to disk
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": new_filename,
            "file_type": file_type,
            "path": str(file_path),
            "content_type": file.content_type
        } # type: ignore
