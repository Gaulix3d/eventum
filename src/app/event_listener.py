import asyncio
import functools
import orjson
from src.app.connection import WSConnection


class EventListener:
    def __init__(self):
        self.events = {}

    async def route_event(self, event: str, data: dict, connection: WSConnection):
        print(connection, data)
        event_path = self.events.get(event)
        if event_path:
            handler = event_path['handler']
            await handler(connection=connection, data=data)
        else:
            print("no event route")

    def event_dec(self, event_name, validator=None):
        def decorator(func):
            @functools.wraps(func)
            async def wrapped_handler(connection: WSConnection, data, *args, **kwargs):
                return await func(connection, data, *args, **kwargs)
            self.events[event_name] = {'handler': wrapped_handler, 'validator': validator}
            return wrapped_handler
        return decorator

    async def listen(self, connection: WSConnection):
        while True:
            message = await connection.receive_text()
            if message:
                try:
                    json_message = self.parse_message(message)
                    event = json_message.get('event')
                    if event:
                        await self.route_event(connection=connection, event=event, data=json_message)
                except Exception as e:
                    raise e

    @staticmethod
    def parse_message(message: str):
        try:
            json_message = orjson.loads(message)
            return json_message
        except orjson.JSONDecodeError as e:
            raise e
