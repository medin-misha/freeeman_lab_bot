from core import rmq_router
from config import settings


async def publish_diagnostic_request(diagnostic_instance: dict):
    await rmq_router.broker.publish(
        message=diagnostic_instance,
        queue=settings.rmq.diagnostic_request_queue
    )


async def publish_diagnostic_response(chat_id: str, file_id: int):
    await rmq_router.broker.publish(
        message={"chat_id": chat_id, "file_id": file_id},
        queue=settings.rmq.diagnostic_response_queue,
    )
