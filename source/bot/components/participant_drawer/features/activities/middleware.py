import logging
from typing import Any, Awaitable, Callable, Dict, Tuple

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject


class RestoreDataMiddleware(BaseMiddleware):
    """Saves a value from FSMContext by the name,
    passes it to the handler in the data with the name as a key
    and restores it after"""

    def __init__(self, *names: Tuple[str]):
        unique = set(names)
        if len(unique) != names:
            raise ValueError("All names must be unique")

        self.names = unique
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        state: FSMContext | None = data.get("state")
        if state is None:
            return await handler(event, data)

        storage = {}
        state_data = await state.get_data()
        for name in state_data.keys() & self.names:
            storage[name] = state_data.pop(name)

        if len(storage) == 0:
            return await handler(event, data)

        data.update(**storage)
        await state.set_data(state_data)
        try:
            result = await handler(event, data)
        except Exception as e:
            result = None
            logging.exception(msg=e)
        
        finally:
            state_data = await state.get_data()
            if len(state_data.keys() & self.names) != 0:
                repeated = state_data.keys() & self.names
                if len(repeated) > 1:
                    raise KeyError(
                        f"Keys {', '.join(repeated)} needs to be restored, but it's already in use"
                    )
                raise KeyError(
                    f"Key {repeated.pop()} needs to be restored, but it's already in use"
                )

            await state.update_data(**storage)
            return result
