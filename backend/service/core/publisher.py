from typing import Any, Mapping

from core import rmq_router
from config import settings


def _serialize_message(message: Mapping[str, Any]) -> dict[str, Any]:
    return dict(message)


async def publish_core_application(application: Mapping[str, Any]) -> None:
    await rmq_router.broker.publish(
        message=_serialize_message(application),
        queue=settings.rmq.nucleus_application_queue,
    )
