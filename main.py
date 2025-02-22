import os
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum
from starlette.staticfiles import StaticFiles

from common.constant import STATIC_DIR_NAME
from common.create_seed_data import seed_data
from config.db import get_db_session
from config.setting import settings
from routers import routers

router = APIRouter()


@asynccontextmanager
async def lifespan(my_app: FastAPI):
    print(f"Starting up...{my_app.title}")
    for session in get_db_session():
        seed_data(session)
    yield  # Application starts here
    # Shutdown event - your previous shutdown code goes here
    print("Shutting down...")


app = FastAPI(
    title=settings.title,
    version=settings.version,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
    root_path=settings.root_prefix,
    dependencies=[],
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(STATIC_DIR_NAME, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR_NAME), name="static")


@app.get("/ping", include_in_schema=False)
def index():
    return {"pong": datetime.utcnow().isoformat()}


for router in routers:
    app.include_router(router, prefix=settings.api_router_prefix)


handler = Mangum(app=app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
