import docker
from docker.errors import DockerException
from fastapi import Request


class DockerClient:
    """Lazily connects to the local Docker daemon."""

    def __init__(self) -> None:
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = docker.from_env()
        return self._client

    def available(self) -> bool:
        try:
            self.client.ping()
            return True
        except DockerException:
            return False


def get_docker(request: Request) -> DockerClient:
    return request.app.state.docker
