from __future__ import annotations

from typing import Any

import aiohttp

from config import settings


class API:
    def __init__(self, url: str | None = None) -> None:
        self.url = (url or settings.api_url).rstrip("/")

    def build_url(self, path: str) -> str:
        return f"{self.url}/{path.lstrip('/')}"

    async def post(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.build_url(path), json=data) as response:
                response.raise_for_status()
                return await response.json()


class UserAPI(API):
    async def add_user(
        self,
        username: str,
        email: str,
        phone: str,
        first_name: str,
        last_name: str,
        chat_id: str,
    ) -> dict[str, Any]:
        payload = {
            "username": username,
            "email": email,
            "phone": phone,
            "first_name": first_name,
            "last_name": last_name,
            "chat_id": chat_id,
        }
        return await self.post("/users", payload)
