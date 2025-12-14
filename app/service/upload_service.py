import os
import uuid
from fastapi import UploadFile, HTTPException
from typing import Dict

ALLOWED_FILE_TYPES = {
    "image": ["image/jpeg", "image/png", "image/gif"],
    "audio": ["audio/mpeg", "audio/wav"],
    "video": ["video/mp4", "video/mkv"],
    "doc": ["application/pdf", "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
    "other": []
}

UPLOAD_ROOT = "uploads"  # base folder


class UploadService:
    @staticmethod
    async def save_file(file: UploadFile, type_folder: str) -> Dict[str, str]:
        # Generate unique filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4()}{ext}"
        folder_path = os.path.join(UPLOAD_ROOT, type_folder)

        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, unique_name)

        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate MIME type
        if file.content_type not in ALLOWED_FILE_TYPES.get(type_folder, []):
            # Delete the file if invalid
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Invalid file type: Only {type_folder} supported ")

        return {"filename": unique_name, "path": file_path}
