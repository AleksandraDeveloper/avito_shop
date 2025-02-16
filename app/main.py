from fastapi import FastAPI
from .api.endpoints import router
from .database import Base, engine
from .db.init_db import init_db

Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(
    title="API Avito shop",
    description="API для магазина мерча",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to API Avito shop"}