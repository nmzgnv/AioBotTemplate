import json
from typing import Union, Optional, AnyStr, Dict

from aiogram.dispatcher.storage import BaseStorage

from models import db
from models import User


class GinoStorage(BaseStorage):

    async def close(self):
        await db.pop_bind().close()

    async def wait_closed(self):
        pass

    @classmethod
    def check_address(cls, *,
                      chat: Union[str, int, None] = None,
                      user: Union[str, int, None] = None,
                      ) -> (str, str):
        """
        In all storage's methods chat or user is always required.
        If one of them is not provided, you have to set missing value based on the provided one.
        This method performs the check described above.
        :param chat: chat_id
        :param user: user_id
        :return:
        """
        if chat is None and user is None:
            raise ValueError('"user" or "chat" parameter is required but no one is provided!')

        if user is None:
            user = chat
        elif chat is None:
            chat = user

        return str(chat), str(user)

    async def set_state(self, *,
                        chat: Union[str, int, None] = None,
                        user: Union[str, int, None] = None,
                        state: Optional[AnyStr] = None):
        chat_id, user_id = self.check_address(chat=chat, user=user)
        user = await User.get(user_id)

        resolved_state = self.resolve_state(state) if state is not None else None
        await user.update(state=resolved_state).apply()

    async def get_state(self, *, chat: Union[str, int, None] = None, user: Union[str, int, None] = None,
                        default: Optional[str] = None) -> Optional[str]:
        chat_id, user_id = self.check_address(chat=chat, user=user)
        user = await User.get(user_id)

        if user and user.state:
            return user.state

        return self.resolve_state(default)

    async def set_data(self, *, chat: Union[str, int, None] = None, user: Union[str, int, None] = None,
                       data: Dict = None):
        chat_id, user_id = self.check_address(chat=chat, user=user)
        user = await User.get(user_id)

        await user.update(state_data=json.dumps(data)).apply()

    async def get_data(self, *, chat: Union[str, int, None] = None, user: Union[str, int, None] = None,
                       default: Optional[dict] = None) -> Dict:
        chat_id, user_id = self.check_address(chat=chat, user=user)
        user = await User.get(user_id)

        if user.state_data:
            return json.loads(user.state_data)

        return default or {}

    async def update_data(self, *, chat: Union[str, int, None] = None, user: Union[str, int, None] = None,
                          data: Dict = None, **kwargs):
        if data is None:
            return

        saved_data = await self.get_data(chat=chat, user=user, default={})
        saved_data.update(data, **kwargs)

        await self.set_data(chat=chat, user=user, data=saved_data)

    def has_bucket(self):
        return False

    async def get_bucket(self, *,
                         chat: Union[str, int, None] = None,
                         user: Union[str, int, None] = None,
                         default: Optional[dict] = None) -> Dict:
        raise NotImplementedError

    async def set_bucket(self, *,
                         chat: Union[str, int, None] = None,
                         user: Union[str, int, None] = None,
                         bucket: Dict = None):
        raise NotImplementedError

    async def update_bucket(self, *,
                            chat: Union[str, int, None] = None,
                            user: Union[str, int, None] = None,
                            bucket: Dict = None,
                            **kwargs):
        raise NotImplementedError

    async def reset_bucket(self, *,
                           chat: Union[str, int, None] = None,
                           user: Union[str, int, None] = None):
        await self.set_data(chat=chat, user=user, data={})
