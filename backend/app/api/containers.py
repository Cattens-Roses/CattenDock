import docker
from fastapi import APIRouter, Depends, HTTPException

from app.core.docker_client import DockerClient, get_docker

router = APIRouter()


def _require(docker: DockerClient) -> DockerClient:
    if not docker.available():
        raise HTTPException(503, "Docker daemon not reachable")
    return docker


@router.get("/")
def list_containers(docker: DockerClient = Depends(get_docker)):
    _require(docker)
    out = []
    for c in docker.client.containers.list(all=True):
        image = c.image.tags[0] if c.image.tags else c.image.short_id
        out.append(
            {
                "id": c.short_id,
                "name": c.name,
                "image": image,
                "status": c.status,
            }
        )
    return out


@router.post("/{container_id}/start")
def start_container(container_id: str, docker: DockerClient = Depends(get_docker)):
    _require(docker)
    try:
        docker.client.containers.get(container_id).start()
    except docker.errors.NotFound:
        raise HTTPException(404, "container not found")
    return {"ok": True}


@router.post("/{container_id}/stop")
def stop_container(container_id: str, docker: DockerClient = Depends(get_docker)):
    _require(docker)
    try:
        docker.client.containers.get(container_id).stop()
    except docker.errors.NotFound:
        raise HTTPException(404, "container not found")
    return {"ok": True}


@router.delete("/{container_id}")
def remove_container(container_id: str, docker: DockerClient = Depends(get_docker)):
    _require(docker)
    try:
        docker.client.containers.get(container_id).remove(force=True)
    except docker.errors.NotFound:
        raise HTTPException(404, "container not found")
    return {"ok": True}
