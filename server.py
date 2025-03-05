import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles


import subprocess

try:
    # Run 'ldd --version' command to get glibc version
    result = subprocess.run(['ldd', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    glibc_version = result.stdout.decode('utf-8').splitlines()[0]
    print(f"glibc version: {glibc_version}")
except Exception as e:
    print(f"Error occurred: {e}")

# exit()

import importlib.util
import sys

# Specify the path to the .so file (extension module)
so_file_path = "PyChessBot.cpython-310-x86_64-linux-gnu.so"
module_name = "PyChessBot"

# Load the module
spec = importlib.util.spec_from_file_location(module_name, so_file_path)
PyChessBot = importlib.util.module_from_spec(spec)
sys.modules[module_name] = PyChessBot
spec.loader.exec_module(PyChessBot)

print(PyChessBot)


app = FastAPI()
app.mount('/static', StaticFiles(directory='static', html=True), name='static')


@app.get('/getMove', response_class=PlainTextResponse)
async def getMove(fen: str):
    bot = PyChessBot.ChessBot()
    bot.setFen(fen)
    return bot.findMove(5)

uvicorn.run(app, host='0.0.0.0', port=8000)
