import datetime

import pytest  # type: ignore
from src.application import (
    DeletedUserDTO,
    DeleteUserData,
    UserService,
)
from src.domain import UserAggregate
from src.domain.user.exceptions import UserIsDeleted
from src.domain.user.value_objects import (
    UserBirthday,
    UserGender,
    UserId,
)
from src.infrastructure import MapperImpl
from tests.mocks import (
    UserCloudStorageMock,
    UserUoWMock,
)


@pytest.mark.asyncio
async def test_delete_user_correct(
    uow: UserUoWMock, mapper: MapperImpl, cloud_storage_repo: UserCloudStorageMock
) -> None:
    user_service = UserService(uow=uow, mapper=mapper, cloud_storage=cloud_storage_repo)

    user = UserAggregate(
        user_id=UserId(value=0),
        first_name="Danila",
        last_name="Safonov",
        gender=UserGender(value="male"),
        birthday=UserBirthday(value=datetime.date.today()),
    )

    await uow.user_repo.create_user(user=user)

    delete_data = DeleteUserData(user_id=0)

    deleted_user_data = await user_service.delete_user(data=delete_data)

    assert deleted_user_data == DeletedUserDTO(
        user_id=0, first_name="Danila", last_name="Safonov", deleted=True
    )
    assert uow.commit_status is True
    assert uow.rollback_status is False


@pytest.mark.asyncio
async def test_delete_deleted_user(
    uow: UserUoWMock, mapper: MapperImpl, cloud_storage_repo: UserCloudStorageMock
) -> None:
    user_service = UserService(uow=uow, mapper=mapper, cloud_storage=cloud_storage_repo)

    user = UserAggregate(
        user_id=UserId(value=0),
        first_name="Danila",
        last_name="Safonov",
        gender=UserGender(value="male"),
        birthday=UserBirthday(value=datetime.date.today()),
        deleted=True,
    )

    await uow.user_repo.create_user(user=user)

    delete_data = DeleteUserData(user_id=0)

    with pytest.raises(UserIsDeleted):
        await user_service.delete_user(data=delete_data)

    assert uow.commit_status is False
    assert uow.rollback_status is False
