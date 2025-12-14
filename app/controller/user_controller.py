from fastapi import APIRouter,Depends, UploadFile,File
from app.models.user_profile_model import UserProfile
from app.schemas.request.user_request_schema import UpdateUserProfile
from app.dependencies.auth import require_roles
from app.enums.user_enum import UserRole
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.models.user_model import User
from app.service.user_service import UserService
from typing import Optional
from app.service.upload_service import UploadService
from app.dependencies.form_data import validate_form_data

router=APIRouter(prefix="/user",tags=["user"])

@router.patch("/update-profile",response_model=UserProfile)
async def update_user_profile(data: UpdateUserProfile = Depends(validate_form_data(UpdateUserProfile)),file: Optional[UploadFile] = File(None),
current_user:User=Depends(require_roles([UserRole.USER])),db:AsyncSession=Depends(get_session)):
    
    update_data = data.model_dump(exclude_unset=True)

    print(update_data,"----->")

    if file:
        upload_result = await UploadService.save_file(file) # type: ignore
        update_data["image"] = upload_result["path"]
        update_data["image_id"] = upload_result["filename"]
    result=await UserService.update_user_profile(db,update_data,current_user.id)

    return result