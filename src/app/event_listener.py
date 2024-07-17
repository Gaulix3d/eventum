import functools
import orjson
from src.app.connection import WSConnection
from src.app.connections import Connections


class EventListener:
    def __init__(self, connections: Connections):
        self.connections = connections
        self.events = {}

    #TODO: finish tomorrow
    def route_event(self, event: str, data: dict):
        pass

    def event_dec(self, event_name, validator=None):
        def decorator(func):
            @functools.wraps(func)
            async def wrapped_handler(connection: WSConnection, *args, **kwargs):
                return await func(connection, *args, **kwargs)
            self.events[event_name] = {'handler': wrapped_handler, 'validator': validator}
            return wrapped_handler
        return decorator

    async def print_them(self):
        while True:
            async for connection in self.connections:
                data = await connection.receive_text()
                if data:
                    print(data)

    @staticmethod
    def parse_event(event: str):
        try:
            orjson.loads(event)
        except orjson.JSONDecodeError as e:
            raise e
