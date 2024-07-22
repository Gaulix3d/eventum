from src.app.middlewares import Middleware
from src.app.middlewares.exceptions_middleware import ExceptionMiddleware
from src.app.middlewares.server_error_middleware import ServerErrorMiddleware


class MiddlewareChain:
    def __init__(self, router):
        self.__user_middlewares = []
        self.router = router

    def add_user_middleware(self, middleware):
        self.__user_middlewares.append(middleware)

    def construct_middleware(self):
        middleware = (
                [Middleware(ServerErrorMiddleware)]
                + self.__user_middlewares
                + [Middleware(ExceptionMiddleware)]
        )
        call_next = self.router
        for cls, args, kwargs in reversed(middleware):
            call_next = cls(call_next=call_next, *args, **kwargs)
        return call_next

