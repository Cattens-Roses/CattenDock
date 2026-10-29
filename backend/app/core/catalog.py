import os
from pathlib import Path

import yaml

CATALOG_DIR = Path(__file__).resolve().parents[3] / "catalog"

DEFAULTS = {
    "CONFIG_PATH": "/opt/cattendock/apps",
    "DATA_PATH": "/opt/cattendock/data",
    "MEDIA_PATH": "/srv/media",
}


def _expand(value: str) -> str:
    for key, default in DEFAULTS.items():
        value = value.replace(f"${{{key}}}", os.environ.get(key, default))
    return value


def load_apps() -> list[dict]:
    if not CATALOG_DIR.exists():
        return []
    apps = []
    for path in sorted(CATALOG_DIR.glob("*.yaml")):
        with path.open() as fh:
            spec = yaml.safe_load(fh)
        spec["id"] = path.stem
        apps.append(spec)
    return apps


def load_app(app_id: str) -> dict | None:
    path = CATALOG_DIR / f"{app_id}.yaml"
    if not path.exists():
        return None
    with path.open() as fh:
        spec = yaml.safe_load(fh)
    spec["id"] = app_id
    return spec


def expanded_docker_spec(spec: dict) -> dict:
    docker = dict(spec.get("docker", {}))
    docker["ports"] = [_expand(p) for p in docker.get("ports", [])]
    docker["volumes"] = [_expand(v) for v in docker.get("volumes", [])]
    docker["environment"] = {
        k: _expand(str(v)) for k, v in docker.get("environment", {}).items()
    }
    return docker
