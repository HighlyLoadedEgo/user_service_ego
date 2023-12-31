from src.application.common import (
    Mapper,
    Service,
)
from src.application.user import (
    dto,
    s3,
    use_cases,
)
from src.application.user.uow import UserUoW


class UserService(Service):
    """
    Сервис который отвечает за работу с Пользователем
    """

    def __init__(
        self, *, uow: UserUoW, mapper: Mapper, cloud_storage: s3.UserCloudStorage
    ) -> None:
        self._uow = uow
        self._mapper = mapper
        self._cloud_storage = cloud_storage

    async def get_user(self, data: use_cases.GetUserData) -> dto.UserDTO:
        """
        Получение полных данных о пользователе
        """
        return await use_cases.GetUser(uow=self._uow, mapper=self._mapper)(data=data)

    async def create_user(self, data: use_cases.CreateUserData) -> dto.UserDTO:
        """
        Сохранение данных пользователя в бд
        """
        return await use_cases.CreateUser(uow=self._uow, mapper=self._mapper)(data=data)

    async def update_user(self, data: use_cases.UpdateUserData) -> dto.UserDTO:
        """
        Обновление данных пользователя
        """
        return await use_cases.UpdateUser(uow=self._uow, mapper=self._mapper)(data=data)

    async def delete_user(self, data: use_cases.DeleteUserData) -> dto.DeletedUserDTO:
        """
        Смена значений флага deleted в бд
        """
        return await use_cases.DeleteUser(uow=self._uow, mapper=self._mapper)(data=data)

    async def set_avatar(self, data: use_cases.SetAvatarData) -> dto.AvatarDTO:
        """
        Установить аватарку пользователю
        """
        return await use_cases.SetAvatar(
            uow=self._uow, mapper=self._mapper, cloud_storage=self._cloud_storage
        )(data=data)

    async def delete_avatar(
        self, data: use_cases.DeleteAvatarData
    ) -> dto.DeletedAvatarDTO | None:
        """
        Удаление аватарки
        """
        return await use_cases.DeleteAvatar(
            uow=self._uow, mapper=self._mapper, cloud_storage=self._cloud_storage
        )(data=data)

    async def subscribe(self, data: use_cases.SubscribeData) -> dto.SubscribeActionDTO:
        """
        Подписаться на пользователя
        """
        return await use_cases.Subscribe(uow=self._uow, mapper=self._mapper)(data=data)

    async def get_subscribers(
        self, data: use_cases.GetSubscribersData
    ) -> dto.SubscribersDTO:
        """
        Получить всех подписчиков
        """
        return await use_cases.GetSubscribers(uow=self._uow)(data=data)

    async def get_subscriptions(
        self, data: use_cases.GetSubscriptionsData
    ) -> dto.SubscriptionsDTO:
        """
        Получить все подписки
        """
        return await use_cases.GetSubscriptions(uow=self._uow)(data=data)

    async def unsubscribe(
        self, data: use_cases.UnsubscribeData
    ) -> dto.SubscribeActionDTO:
        """
        Отписаться от пользователя
        """
        return await use_cases.Unsubscribe(uow=self._uow, mapper=self._mapper)(
            data=data
        )
