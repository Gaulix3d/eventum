from src.app.connection import WSConnection
from src.app.event_listener import EventListener
from src.app.lifespan import Lifespan
from src.app.middleware_chain import MiddlewareChain
from src.app.routing import Router


class Eventum:
    def __init__(self):
        self.middleware_stack = None
        self.event_listener = EventListener()
        self.router = Router(event_listener=self.event_listener)
        self.__middleware_constr = MiddlewareChain(router=self.router)
        self.lifespan = Lifespan()

    async def __call__(self, scope, receive, send):
        scope['app'] = self
        if scope['type'] == 'lifespan':
            await self.lifespan(scope=scope, receive=receive, send=send)
        else:
            connection = WSConnection(scope=scope, receive=receive, send=send)
            if self.middleware_stack is None:
                self.construct_middleware()
            await self.middleware_stack(connection)

    def construct_middleware(self):
        self.middleware_stack = self.__middleware_constr.construct_middleware()

    def route(self, path):
        return self.router.route(path=path)

    def event(self, event, validator=None):
        return self.event_listener.event_dec(event, validator=validator)

    def on_startup(self):
        return self.lifespan.on_startup_dec()

    def on_shutdown(self):
        return self.lifespan.on_shutdown_dec()
