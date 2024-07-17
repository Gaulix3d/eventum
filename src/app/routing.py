import functools
from src.app.connection import WSConnection


class Router:
    def __init__(self):
        self.routes = {}

    async def __call__(self, connection: WSConnection):
        path = self.routes.get(connection.path)
        if path:
            handler = path['handler']
            await handler(connection)
        else:
            print("no route")

    def route(self, path):
        def decorator(func):
            @functools.wraps(func)
            async def wrapped_handler(connection: WSConnection, *args, **kwargs):
                return await func(connection, *args, **kwargs)
            self.routes[path] = {'handler': wrapped_handler}
            return wrapped_handler
        return decorator






