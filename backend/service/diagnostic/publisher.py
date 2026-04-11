from typing import Any, Mapping

from pydantic import BaseModel

from core import rmq_router
from config import settings


def _serialize_message(message: BaseModel | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(message, BaseModel):
        return message.model_dump(mode="json")

    return dict(message)


async def publish_diagnostic_request(diagnostic_instance: BaseModel | Mapping[str, Any]):
    await rmq_router.broker.publish(
        message=_serialize_message(diagnostic_instance),
        queue=settings.rmq.diagnostic_request_queue,
    )


async def publish_diagnostic_response(chat_id: str, file_id: int):
    await rmq_router.broker.publish(
        message={"chat_id": chat_id, "file_id": file_id},
        queue=settings.rmq.diagnostic_response_queue,
    )
