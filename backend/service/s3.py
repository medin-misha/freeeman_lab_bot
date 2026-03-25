from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from .error_handlers import S3ErrorHandler
from config import settings


class S3Client:
    def __init__(
        self,
        bucket_name: str = settings.s3.bucket_name,
        endpoint_url: str = settings.s3.endpoint_url,
        aws_access_key_id: str = settings.s3.access_key,
        aws_secret_access_key: str = settings.s3.secret_key,
    ):
        self.config: dict = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name: str = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
        self, file: bytes, object_name: str, folder: str = None, filename: str = None
    ):
        key = f"{folder}/{object_name}{filename}"
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=file,
                )
        except Exception as e:
            S3ErrorHandler.handle(e, "upload file")
        else:
            return key

    async def get_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                return await response["Body"].read()
        except Exception as e:
            S3ErrorHandler.handle(e, "get file")
