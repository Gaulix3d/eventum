class WSConnection:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self.receive = receive
        self.send = send
        self.extra_headers = []
        self.active = False
        self.authenticated = False

    async def accept(self):
        self.__add_subprotocol_to_response()
        response_dict = {
            "type": "websocket.accept",
            "headers": self.extra_headers
        }
        await self.send(response_dict)
        self.active = True

    async def close(self, code=1000, reason=""):
        print(reason)
        await self.send({
            "type": "websocket.close",
            "code": code,
            "reason": reason
        })
        self.active = False

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

    def __add_subprotocol_to_response(self):
        if self.subprotocols:
            self.extra_headers.append((
                'Sec-WebSocket-Protocol'.encode(),
                self.subprotocols[0].encode()
            ))

    def add_header(self, header_name, header_value):
        self.extra_headers.append((
            header_name.encode(),
            header_value.encode()
        ))

    def add_headers(self, headers_dict):
        for header_name, header_value in headers_dict:
            self.extra_headers.append((
                header_name.encode(),
                header_value.encode()
            ))

    async def send_ping(self):
        await self.send({
            "type": "websocket.ping"
        })

    @property
    def path(self):
        return self.scope.get('path')

    @property
    def subprotocols(self):
        return self.scope.get('subprotocols')
