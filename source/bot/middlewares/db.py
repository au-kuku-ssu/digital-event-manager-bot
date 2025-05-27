from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Dict, Any, Callable, Awaitable

from components.shared.db import Database

import sys


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db: Database, log_str: str):
        self.db = db
        sys.stdout.write(f"INFO: {log_str} Middlefare is up\n")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Database],
    ) -> Any:
        data["db"] = self.db
        return await handler(event, data)
