from typing import Callable

from src.app.connection import WSConnection


class ServerErrorMiddleware:
    def __init__(self, call_next: Callable) -> None:
        self.call_next = call_next

    async def __call__(self, connection: WSConnection) -> None:
        try:
            await self.call_next(connection)
            return
        except Exception as e:
            print(e)


