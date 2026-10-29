from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import catalog, containers, system
from app.core.docker_client import DockerClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.docker = DockerClient()
    yield


app = FastAPI(title="CattenDock API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(containers.router, prefix="/api/containers", tags=["containers"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(catalog.router, prefix="/api/catalog", tags=["catalog"])

# Serve the built frontend if present (production)
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
