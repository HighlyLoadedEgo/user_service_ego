from abc import (
    ABC,
    abstractmethod,
)

from src.application.common import CloudStorageBase
from src.application.user.use_cases.avatar.set_avatar import SetAvatarData
from src.domain import AvatarEntity


class UserCloudStorage(CloudStorageBase, ABC):
    @abstractmethod
    async def put(self, avatar: SetAvatarData) -> None:
        """Сохранение объекта"""

    @abstractmethod
    async def delete(self, avatar: AvatarEntity) -> None:
        """Удаление объекта"""
