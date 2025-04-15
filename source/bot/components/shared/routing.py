from aiogram import Router, types
from aiogram.filters import Command
from typing import Callable, Any
from functools import partial

def create_callback_handler(
    router: Router,
    callback_data: str,
    handler_func: Callable,
    **filter_kwargs
) -> None:
    """
    Создает обработчик callback-запросов с заданными параметрами

    :param router: Роутер, к которому будет привязан обработчик
    :param callback_data: Значение callback_data для фильтрации
    :param handler_func: Функция-обработчик
    :param filter_kwargs: Дополнительные параметры для фильтра
    """
    decorator = router.callback_query(lambda c: c.data == callback_data, **filter_kwargs)

    async def wrapper(callback_query: types.CallbackQuery, bot: Any) -> None:
        await handler_func(callback_query, bot)

    decorator(wrapper)

def setup_callbacks(router: Router, handlers_map: dict[str, Callable]) -> None:
    """
    Настраивает несколько обработчиков callback-запросов

    :param router: Роутер для регистрации обработчиков
    :param handlers_map: Словарь {callback_data: handler_function}
    """
    for callback_data, handler_func in handlers_map.items():
        create_callback_handler(router, callback_data, handler_func)
