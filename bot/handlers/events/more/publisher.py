from __future__ import annotations

from typing import Any, Mapping

from faststream.rabbit import RabbitBroker

from config import settings

broker = RabbitBroker(settings.rmq_url)


async def publish_consultation_request(data: Mapping[str, Any]) -> None:
    await broker.publish(
        message=dict(data),
        queue=settings.consultation_request_queue,
    )


async def publish_regression_request(data: Mapping[str, Any]) -> None:
    await broker.publish(
        message=dict(data),
        queue=settings.regression_request_queue,
    )


async def publish_mentorship_request(data: Mapping[str, Any]) -> None:
    await broker.publish(
        message=dict(data),
        queue=settings.mentorship_request_queue,
    )
