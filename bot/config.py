from pathlib import Path
import json
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Messages:
    with open(BASE_DIR / "messages.json", "r", encoding="utf-8") as f:
        text: dict = json.load(f)

class Files:
    scale_file_pdf: str = BASE_DIR / "files" / "documents" / "Потолок_внутри_код_расширения_Методичка_апрель.pdf"
    scale_file_epub: str = BASE_DIR / "files" / "documents" / "Потолок_внутри_код_расширения_Методичка_апрель.epub"
    scale_file_video: str = BASE_DIR / "files" / "videos" / "sircle2.mp4"
    expanded_diagnostic_video: str = BASE_DIR / "files" / "videos" / "sircle3.mp4"
    expanded_diagnostic_intro_video: str = BASE_DIR / "files" / "videos" / "sircle4.mp4"
    diagnostic_result_video: str = BASE_DIR / "files" / "videos" / "sircle5.mp4"
    nucleus_intro_video: str = BASE_DIR / "files" / "videos" / "sircle6.mp4"
    analysis_file_pdf: str = BASE_DIR / "files" / "documents" / "ДИАГНОСТИЧЕСКАЯ_ИНСТРУКЦИЯ_КАРТА_МАСШТАБА_ПОТОЛК_ВНУТРИ_КОД_РАСШИРЕНИЯ.pdf"
    wording_of_request_for_analysis: str = BASE_DIR / "files" / "documents" / "Как_правильно_формулировать_запрос.pdf"
    subscribe_preview_image: str = BASE_DIR / "files" / "images" / "preview.jpg"
    subscribe_video: str = BASE_DIR / "files" / "videos" / "sircle1.mp4"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    token: str = Field(validation_alias="TOKEN")
    api_url: str = Field(validation_alias="API_URL")
    telegram_bot_api_url: str = Field(validation_alias="TELEGRAM_BOT_API_URL")
    channel_id: str = Field(validation_alias="CHANNEL_ID")
    rmq_url: str = Field(validation_alias="RMQ_URL")
    diagnostic_response_queue: str = Field(
        validation_alias="RMQ_DIAGNOSTIC_RESPONSE_QUEUE"
    )
    nucleus_application_queue: str = Field(
        default="nucleus_application",
        validation_alias="RMQ_NUCLEUS_APPLICATION_QUEUE"
    )
    message: Messages = Messages()
    files: Files = Files()

settings = Settings()
