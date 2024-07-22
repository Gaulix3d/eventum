from src.app.connection import WSConnection
from src.app.exceptions.ws_exception import WSException
from src.app.middlewares import _MiddlewareClass


class ExceptionMiddleware:
    def __init__(self, call_next: _MiddlewareClass) -> None:
        self.call_next = call_next

    async def __call__(self, connection: WSConnection) -> None:
        try:
            await self.call_next(connection)
        except WSException as e:
            await self.handle_exc(exception=e,
                                  connection=connection
                                  )

    @staticmethod
    async def handle_exc(exception: WSException,
                         connection: WSConnection):
        if isinstance(exception, WSException):
            await connection.close(code=exception.code, reason=exception.reason)



