import imghdr
from typing import Union

from fastapi import (
    APIRouter,
    Depends,
    Header,
    UploadFile,
    status,
)
from src.application import (
    AvatarIsNotExist,
    DeleteAvatarData,
    SetAvatarData,
    UserIsNotExist,
)
from src.application.user.service.user_service import UserService
from src.domain.user.exceptions import InvalidAvatarType
from src.presentation.api.controllers import response as resp
from src.presentation.api.controllers.response import (
    DeletedAvatarResponse,
    SetAvatarResponse,
)
from src.presentation.api.di import get_service_stub

avatar_routers = APIRouter(tags=["avatars"], prefix="/avatars")


@avatar_routers.post(
    path="/set_avatar",
    responses={
        status.HTTP_201_CREATED: {"model": SetAvatarResponse},
        status.HTTP_400_BAD_REQUEST: {
            "model": resp.ErrorResult[Union[InvalidAvatarType]]
        },
        status.HTTP_404_NOT_FOUND: {"model": resp.ErrorResult[UserIsNotExist]},
    },
    response_model=SetAvatarResponse,
)
async def set_avatar(
    avatar_data: UploadFile,
    service: UserService = Depends(get_service_stub),
    x_user_id: int = Header(None),
):
    """
    Установка аватарки у пользователя
    """
    file = avatar_data.file.read()
    file_type = imghdr.what(None, file)

    data = SetAvatarData(
        avatar_content=file,
        avatar_user_id=x_user_id,
        avatar_type=file_type if file_type else "none_type",
    )  # type: ignore

    return await service.set_avatar(data=data)


@avatar_routers.delete(
    path="/delete_avatar",
    responses={
        status.HTTP_200_OK: {"model": DeletedAvatarResponse},
        status.HTTP_404_NOT_FOUND: {"model": AvatarIsNotExist},
    },
    response_model=DeletedAvatarResponse,
)
async def delete_avatar(
    service: UserService = Depends(get_service_stub), x_user_id: int = Header(None)
):
    """
    Удаление аватарки у пользователя
    """
    return await service.delete_avatar(data=DeleteAvatarData(user_id=x_user_id))
