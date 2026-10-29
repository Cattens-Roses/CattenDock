import socket
import time

import psutil
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def stats():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "hostname": socket.gethostname(),
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "memory": {
            "total": mem.total,
            "used": mem.used,
            "percent": mem.percent,
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "percent": disk.percent,
        },
    }
