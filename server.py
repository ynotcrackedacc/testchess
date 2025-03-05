import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import PyChessBot
import os

print(os.getcwd())
print(os.listdir())

app = FastAPI()
app.mount('/static', StaticFiles(directory='static', html=True), name='static')


@app.get('/getMove', response_class=PlainTextResponse)
async def getMove(fen: str):
    bot = PyChessBot.ChessBot()
    bot.setFen(fen)
    return bot.findMove(3)

uvicorn.run(app, host='0.0.0.0', port=8000)
