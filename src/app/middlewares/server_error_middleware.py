import traceback
from typing import Any
from src.app.connection import WSConnection
from src.app.middlewares import _MiddlewareClass


class ServerErrorMiddleware(_MiddlewareClass):
    def __init__(self, call_next: _MiddlewareClass, *args: Any, **kwargs: Any) -> None:
        self.call_next = call_next

    async def __call__(self, connection: WSConnection) -> None:
        try:
            await self.call_next(connection)
        except Exception as e:
            traceback.print_exception(e)
