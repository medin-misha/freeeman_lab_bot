from faststream.rabbit import RabbitBroker

from config import settings


broker = RabbitBroker(settings.rmq_url)
