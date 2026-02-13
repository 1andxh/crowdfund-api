from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router

version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting...")
    await init_db()

    yield
    print("server is stopping")


app = FastAPI(
    version=version,
    title="Fundly-API",
    description="RESTful API for creating crowdfunding campaigns, processing donations, and managing fundraising data securely and at scale.",
    lifespan=lifespan,
)


app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["authentication"])
