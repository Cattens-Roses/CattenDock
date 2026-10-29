import docker
from fastapi import APIRouter, Depends, HTTPException

from app.core import catalog as catalog_core
from app.core.docker_client import DockerClient, get_docker

router = APIRouter()


@router.get("/")
def list_apps():
    return catalog_core.load_apps()


@router.post("/{app_id}/deploy")
def deploy_app(app_id: str, docker: DockerClient = Depends(get_docker)):
    if not docker.available():
        raise HTTPException(503, "Docker daemon not reachable")

    spec = catalog_core.load_app(app_id)
    if spec is None:
        raise HTTPException(404, "app not found")

    d = catalog_core.expanded_docker_spec(spec)
    name = spec.get("id", app_id)

    try:
        container = docker.client.containers.run(
            d["image"],
            name=name,
            detach=True,
            ports=_parse_ports(d["ports"]),
            volumes=d["volumes"],
            environment=d.get("environment") or None,
            restart_policy={"Name": "unless-stopped"},
        )
    except docker.errors.APIError as exc:
        if "Conflict" in str(exc):
            raise HTTPException(409, f"container '{name}' already exists")
        raise HTTPException(500, str(exc))

    return {"ok": True, "id": container.short_id, "name": container.name}


def _parse_ports(ports: list[str]) -> dict:
    out = {}
    for p in ports:
        host, container = p.split(":")
        out[f"{container}/tcp"] = int(host)
    return out
