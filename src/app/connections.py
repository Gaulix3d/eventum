class Connections:
    def __init__(self):
        self.connections = set()

    def add(self, connection):
        self.connections.add(connection)

    def remove(self, connection):
        self.remove(connection)

    def __aiter__(self):
        self.iter_connections = iter(self.connections)
        return self

    async def __anext__(self):
        try:
            return next(self.iter_connections)
        except StopIteration:
            raise StopAsyncIteration
