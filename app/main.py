from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongo import mongo_client

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY,)

@app.on_event("startup")
async def on_startup():
    await mongo_client.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await mongo_client.disconnect()

@app.get("/health")
def healthcheck():
    return {"status": "ok"}

from app.api.v1 import api_router
app.include_router(api_router, prefix="/api/v1")
