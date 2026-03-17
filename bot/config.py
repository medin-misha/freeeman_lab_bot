from pathlib import Path
import json
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Messages:
    with open(BASE_DIR / "messages.json", "r", encoding="utf-8") as f:
        text: dict = json.load(f)

class Files:
    scale_file_pdf: str = BASE_DIR / "files" / "Потолок_внутри_код_расширения_Фриман_Александр.pdf"
    scale_file_epub: str = BASE_DIR / "files" / "Потолок_внутри_код_расширения_Александр_Фриман.epub"
    analysis_file_pdf: str = BASE_DIR / "files" / "ИНСТРУКЦИЯ__ПОДГОТОВКА_К_НЕЙРОЛИНГВИСТИЧЕСКОМУ_РАЗБОРУ.pdf"
    

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    token: str = Field(validation_alias="TOKEN")
    api_url: str = Field(validation_alias="API_URL")
    channel_id: str = Field(validation_alias="CHANNEL_ID")
    message: Messages = Messages()
    files: Files = Files()

settings = Settings()