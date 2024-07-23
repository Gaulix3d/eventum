import functools
from src.app.connection import WSConnection
from src.app.event_listener import EventListener


class Router:
    def __init__(self, event_listener: EventListener):
        self.routes = {}
        self.event_listener = event_listener

    async def __call__(self, connection: WSConnection) -> None:
        path = self.routes.get(connection.path)
        if path:
            handler = path['handler']
            await handler(connection)
            await self.event_listener.listen(connection)
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






