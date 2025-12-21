import os
import uuid
from fastapi import UploadFile, HTTPException
from typing import Dict,List
import aiofiles


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
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")

        # Validate MIME type before writing
        if file.content_type not in ALLOWED_FILE_TYPES.get(type_folder, []):
            raise HTTPException(status_code=400, detail=f"Invalid file type: Only {type_folder} supported")

        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4()}{ext}"
        folder_path = os.path.join(UPLOAD_ROOT, type_folder)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, unique_name)

        # Async save file
        import aiofiles
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        return {"filename": unique_name, "path": file_path}

    
    @staticmethod
    async def save_files_atomic(files: List[UploadFile], type_folder: str) -> List[Dict[str, str]]:
        """
        Save multiple files atomically: all or none.

        Args:
            files: List of UploadFile objects
            type_folder: Type of folder (image, video, audio, doc)

        Returns:
            List of dicts containing filename and path for saved files
        """
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")

        folder_path = os.path.join(UPLOAD_ROOT, type_folder)
        os.makedirs(folder_path, exist_ok=True)

        saved_files: List[Dict[str, str]] = []

        try:
            for file in files:
                if not file.filename:
                    raise HTTPException(status_code=400, detail="One of the files has no filename")

                ext = os.path.splitext(file.filename)[1]
                unique_name = f"{uuid.uuid4()}{ext}"
                file_path = os.path.join(folder_path, unique_name)

                # Validate MIME type before saving
                if file.content_type not in ALLOWED_FILE_TYPES.get(type_folder, []):
                    raise HTTPException(status_code=400, detail=f"Invalid file type for file: {file.filename}")

                # Async write file
                content: bytes = await file.read()
                async with aiofiles.open(file_path, "wb") as f: 
                    await f.write(content)

                saved_files.append({"filename": unique_name, "path": file_path})

        except HTTPException as e:
            # Cleanup any files that were already written if any file fails
            for f in saved_files:
                if os.path.exists(f["path"]):
                    os.remove(f["path"])
            raise e

        return saved_files
    
    @staticmethod
    async def save_multiple_type_files_atomic(files: List[UploadFile], allowed_folders: List[str]) -> List[Dict[str, str]]:
        """
        Save multiple files atomically, allowing only specified type folders.

        Args:
            files: list of UploadFile objects
            allowed_folders: list of allowed type folders, e.g. ["image", "video"]

        Returns:
            List of dicts with filename, original name, type folder, and path
        """
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")

        # Validate allowed folders
        for folder in allowed_folders:
            if folder not in ALLOWED_FILE_TYPES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid allowed folder: {folder}. Only 'image' and 'video' are allowed."
                )

        saved_files: List[Dict[str, str]] = []

        try:
            for file in files:
                if not file.filename:
                    raise HTTPException(status_code=400, detail="File without filename")

                # Find matching folder for this file
                type_folder = None
                for folder in allowed_folders:
                    if file.content_type in ALLOWED_FILE_TYPES[folder]:
                        type_folder = folder
                        break

                if not type_folder:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File {file.filename} has unsupported type. Allowed: {allowed_folders}"
                    )

                folder_path = os.path.join(UPLOAD_ROOT, type_folder)
                os.makedirs(folder_path, exist_ok=True)

                ext = os.path.splitext(file.filename)[1]
                unique_name = f"{uuid.uuid4()}{ext}"
                file_path = os.path.join(folder_path, unique_name)

                content = await file.read()
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(content)

                saved_files.append({
                    "original_name": file.filename,
                    "filename": unique_name,
                    "type": type_folder,
                    "path": file_path
                })

        except Exception as e:
            # Rollback saved files if any failure occurs
            for f in saved_files:
                if os.path.exists(f["path"]):
                    os.remove(f["path"])
            raise e

        return saved_files