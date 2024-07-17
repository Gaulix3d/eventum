import uvicorn
from src.app.app import Eventum
from src.app.connection import WSConnection

app = Eventum()


@app.route('/')
async def index(connection: WSConnection):
    pass


@app.route('/andrey')
async def andrey(connection: WSConnection):
    await connection.accept()
    while True:
        print(await connection.receive_text())

if __name__ == "__main__":
    uvicorn.run(app=app, host='127.0.0.1', port=867)