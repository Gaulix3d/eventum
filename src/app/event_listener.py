from src.app.connections import Connections


class EventListener:
    def __init__(self, connections: Connections):
        self.connections = connections

    async def print_them(self):
        while True:
            async for connection in self.connections:
                data = await connection.receive_text()
                if data:
                    print(data)