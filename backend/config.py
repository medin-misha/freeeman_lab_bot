from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent
SETTINGS_CONFIG = SettingsConfigDict(
    env_file=BASE_DIR / ".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class AppSettings(BaseSettings):
    model_config = SETTINGS_CONFIG

class RMQSettings(AppSettings):
    url: str = Field(validation_alias="RMQ_URL")
    diagnostic_request_queue: str = Field(validation_alias="RMQ_DIAGNOSTIC_REQUEST_QUEUE")
    diagnostic_response_queue: str = Field(validation_alias="RMQ_DIAGNOSTIC_RESPONSE_QUEUE")

class S3Settings(AppSettings):
    access_key: str = Field(validation_alias="AWS_S3_ACCESS_KEY")
    secret_key: str = Field(validation_alias="AWS_S3_SECRERT_KEY")
    bucket_name: str = Field(validation_alias="AWS_S3_BUCKET_NAME")
    endpoint_url: str = Field(validation_alias="AWS_S3_ENDPOINT_URL")


class Settings(AppSettings):
    s3: S3Settings = Field(default_factory=S3Settings)
    rmq: RMQSettings = Field(default_factory=RMQSettings)
    database: str = Field(validation_alias="DATABASE")


settings = Settings()
