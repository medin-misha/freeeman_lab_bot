import asyncio
import logging
from dataclasses import dataclass
from typing import Awaitable, Callable

from sqlalchemy import text

from core import rmq_router
from core.database import database
from service.s3 import S3Client


logger = logging.getLogger(__name__)

CHECK_TIMEOUT_SECONDS = 5.0


@dataclass(slots=True)
class CheckResult:
    status: str
    error: str | None = None

    def as_dict(self) -> dict[str, str]:
        payload = {"status": self.status}
        if self.error is not None:
            payload["error"] = self.error
        return payload


@dataclass(slots=True)
class HealthReport:
    checks: dict[str, CheckResult]

    @property
    def is_ok(self) -> bool:
        return all(check.status == "ok" for check in self.checks.values())

    def as_dict(self) -> dict[str, object]:
        return {
            "status": "ok" if self.is_ok else "fail",
            "checks": {
                component: result.as_dict()
                for component, result in self.checks.items()
            },
        }


def _format_exception(exc: Exception) -> str:
    message = str(exc).strip()
    if not message:
        return type(exc).__name__
    return f"{type(exc).__name__}: {message}"


async def _check_database() -> None:
    async with database.engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


async def _check_rmq() -> None:
    is_alive = await rmq_router.broker.ping(CHECK_TIMEOUT_SECONDS)
    if not is_alive:
        raise RuntimeError("RabbitMQ broker ping returned false")


async def _check_storage() -> None:
    await S3Client().check_bucket()


async def _run_check(
    name: str, check: Callable[[], Awaitable[None]]
) -> tuple[str, CheckResult]:
    try:
        async with asyncio.timeout(CHECK_TIMEOUT_SECONDS):
            await check()
    except Exception as exc:
        logger.exception("Health check failed for %s", name)
        return name, CheckResult(status="fail", error=_format_exception(exc))

    return name, CheckResult(status="ok")


async def collect_health_report() -> HealthReport:
    results = await asyncio.gather(
        _run_check("database", _check_database),
        _run_check("rmq", _check_rmq),
        _run_check("storage", _check_storage),
    )

    checks = {"backend": CheckResult(status="ok")}
    checks.update(dict(results))
    return HealthReport(checks=checks)
