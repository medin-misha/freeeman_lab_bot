from faststream.rabbit.fastapi import RabbitRouter
from config import settings

router = RabbitRouter(url=settings.rmq.url)