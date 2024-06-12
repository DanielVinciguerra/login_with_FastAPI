
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from _app.core.database import create_tables

from _app.views import home_view, error_view
from _app.views.admin import admin_view

import threading
import asyncio
import uvicorn

app = FastAPI(
    exception_handlers=error_view.exception_handlers
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home_view.router)
app.include_router(admin_view.router)

app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')

@app.on_event("startup")
async def startup():
    """EXECUTAR ISSO APENAS 1 VEZ, PARA CRIAR O BANCO DE DADOS"""
    await create_tables()


@app.get('/hello_world')
async def hello_word():
    await asyncio.sleep(0.1)
    return {"hello":"world"}


                    
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
