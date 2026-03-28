import json
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Messages:
    with open(BASE_DIR / "messages.json", "r", encoding="utf-8") as f:
        text: dict = json.load(f)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    token: str = Field(validation_alias="TOKEN")
    api_url: str = Field(validation_alias="API_URL")
    rmq_url: str = Field(validation_alias="RMQ_URL")
    diagnostic_request_queue: str = Field(
        validation_alias="RMQ_DIAGNOSTIC_REQUEST_QUEUE"
    )
    chat_ids: str = Field(validation_alias="CHAT_IDS")
    message: Messages = Messages()

    @field_validator("chat_ids")
    @classmethod
    def validate_chat_ids(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("CHAT_IDS must contain at least one chat id")

        return value

    @property
    def chat_ids_list(self) -> list[int]:
        return [
            int(chat_id.strip())
            for chat_id in self.chat_ids.split(",")
            if chat_id.strip()
        ]


settings = Settings()
