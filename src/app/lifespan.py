import functools


class Lifespan:
    def __init__(self):
        self.on_startup = None
        self.on_shutdown = None

    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'lifespan'
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                if self.on_startup:
                    await self.on_startup()
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                if self.on_shutdown:
                    await self.on_shutdown()
                await send({'type': 'lifespan.shutdown.complete'})
                return

    def on_startup_dec(self):
        def decorator(func):
            @functools.wraps(func)
            async def wrapped_handler(*args, **kwargs):
                return await func(*args, **kwargs)
            self.on_startup = wrapped_handler
            return wrapped_handler
        return decorator

    def on_shutdown_dec(self):
        def decorator(func):
            @functools.wraps(func)
            async def wrapped_handler(*args, **kwargs):
                return await func(*args, **kwargs)
            self.on_shutdown = wrapped_handler
            return wrapped_handler
        return decorator
