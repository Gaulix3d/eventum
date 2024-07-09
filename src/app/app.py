class Eventum:
    def __init__(self):
        pass

    async def __call__(self, scope, receive, send):
        scope['app'] = self


