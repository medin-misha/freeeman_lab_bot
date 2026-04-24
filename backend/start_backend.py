import os
import socket
import subprocess
import sys
import time
from typing import Iterable
from urllib.parse import urlparse


RETRY_INTERVAL_SECONDS = 2.0
CONNECT_TIMEOUT_SECONDS = 3.0

DEFAULT_PORTS = {
    "amqp": 5672,
    "amqps": 5671,
    "http": 80,
    "https": 443,
    "postgres": 5432,
    "postgresql": 5432,
    "postgresql+asyncpg": 5432,
}


def _parse_endpoint(name: str, url: str | None) -> tuple[str, str, int] | None:
    if not url:
        return None

    parsed = urlparse(url)
    if not parsed.hostname:
        raise ValueError(f"{name} has no hostname: {url}")

    port = parsed.port or DEFAULT_PORTS.get(parsed.scheme)
    if port is None:
        raise ValueError(f"{name} has unknown port for scheme '{parsed.scheme}': {url}")

    return name, parsed.hostname, port


def _wait_for_resolution(host: str) -> None:
    socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)


def _wait_for_tcp(host: str, port: int) -> None:
    with socket.create_connection((host, port), timeout=CONNECT_TIMEOUT_SECONDS):
        return


def _wait_for_dependency(name: str, host: str, port: int) -> None:
    attempt = 1
    while True:
        try:
            _wait_for_resolution(host)
            _wait_for_tcp(host, port)
        except OSError as exc:
            print(
                f"[startup] {name} is not ready at {host}:{port} "
                f"(attempt {attempt}): {exc}",
                flush=True,
            )
            attempt += 1
            time.sleep(RETRY_INTERVAL_SECONDS)
            continue

        print(f"[startup] {name} is reachable at {host}:{port}", flush=True)
        return


def _iter_dependencies() -> Iterable[tuple[str, str, int]]:
    candidates = (
        _parse_endpoint("database", os.environ.get("DATABASE")),
        _parse_endpoint("rabbitmq", os.environ.get("RMQ_URL")),
        _parse_endpoint("storage", os.environ.get("AWS_S3_ENDPOINT_URL")),
    )
    return [candidate for candidate in candidates if candidate is not None]


def _run_migrations() -> None:
    print("[startup] applying database migrations", flush=True)
    subprocess.run(
        ["uv", "run", "alembic", "upgrade", "head"],
        check=True,
    )
    print("[startup] database migrations applied", flush=True)


def _start_server() -> None:
    print("[startup] starting backend server", flush=True)
    os.execvp(
        "uv",
        ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    )


def main() -> None:
    for name, host, port in _iter_dependencies():
        _wait_for_dependency(name, host, port)

    _run_migrations()
    _start_server()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[startup] fatal error: {exc}", file=sys.stderr, flush=True)
        raise
