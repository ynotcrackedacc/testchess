import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

import importlib.util
import sys

# Specify the path to the .so file (extension module)
so_file_path = "PyChessBot.cp310-win_amd64.pyd"
module_name = "PyChessBot"

# Load the module
spec = importlib.util.spec_from_file_location(module_name, so_file_path)
PyChessBot = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)

print(PyChessBot)


app = FastAPI()
app.mount('/static', StaticFiles(directory='static', html=True), name='static')


@app.get('/getMove', response_class=PlainTextResponse)
async def getMove(fen: str):
    bot = PyChessBot.ChessBot()
    bot.setFen(fen)
    return bot.findMove(3)

uvicorn.run(app, host='0.0.0.0', port=8000)
