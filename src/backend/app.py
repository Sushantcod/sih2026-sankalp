from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.backend.database import init_db
from src.backend.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema on startup
    init_db()
    yield

app = FastAPI(
    title="SIH 2026 Central Backend Ingestion API",
    description="Central Backend Ingestion Layer for Smart Road Damage, Traffic Density, and ANPR Events.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.backend.app:app", host="0.0.0.0", port=8000, reload=True)
