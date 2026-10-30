from fastapi import FastAPI

from src.api.router import router

app = FastAPI()

app.include_router(router, tags=["Research Papers"])