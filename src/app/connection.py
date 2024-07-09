class WSConnection:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self.receive = receive
        self.send = send

    async def accept(self):
        await self.send({
            "type": "websocket.accept",
        })

    async def close(self, code=1000):
        await self.send({
            "type": "websocket.close",
            "code": code
        })

    async def receive_text(self):
        event = await self.receive()
        if event['type'] == 'websocket.receive':
            return event['text']
        elif event['type'] == 'websocket.disconnect':
            return None

    async def send_text(self, message):
        await self.send({
            "type": "websocket.send",
            "text": message
        })

