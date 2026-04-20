from __future__ import annotations

from typing import Any, Mapping

from faststream.rabbit import RabbitBroker

from config import settings


broker = RabbitBroker(settings.rmq_url)


def _serialize_message(message: Mapping[str, Any]) -> dict[str, Any]:
    return dict(message)


async def publish_analysis_schedule_confirmation(
    confirmation: Mapping[str, Any],
) -> None:
    await broker.publish(
        message=_serialize_message(confirmation),
        queue=settings.analysis_schedule_confirmation_queue,
    )
