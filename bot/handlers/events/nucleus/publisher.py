from typing import Any, Mapping

from faststream.rabbit import RabbitBroker

from config import settings


broker = RabbitBroker(settings.rmq_url)


def _serialize_message(message: Mapping[str, Any]) -> dict[str, Any]:
    return dict(message)


async def publish_nucleus_application(
    application: Mapping[str, Any],
) -> None:
    await broker.publish(
        message=_serialize_message(application),
        queue=settings.nucleus_application_queue,
    )
