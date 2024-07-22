import uvicorn
from src.app.app import Eventum
from src.app.connection import WSConnection
from src.app.exceptions.ws_exception import WSException

app = Eventum()


@app.event('dummy')
async def event_happened(connection: WSConnection, data: dict):
    print(data)
    raise WSException(code=3000, reason='You gay')


@app.route('/')
async def index(connection: WSConnection):
    await connection.accept()


@app.route('/andrey')
async def andrey(connection: WSConnection):
    await connection.accept()
    while True:
        print(await connection.receive_text())

if __name__ == "__main__":
    uvicorn.run(app=app, host='127.0.0.1', port=867)