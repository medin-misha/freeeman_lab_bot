import asyncio
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

import aiohttp


logger = logging.getLogger(__name__)


MessageHandler = Callable[[dict[str, Any]], Awaitable[None]]
CallbackHandler = Callable[[dict[str, Any]], Awaitable[None]]


@dataclass(slots=True)
class TelegramFile:
    content: bytes
    file_path: str


class TelegramBotClient:
    def __init__(self, token: str) -> None:
        self._token = token
        self._base_url = f"https://api.telegram.org/bot{token}"
        self._session: aiohttp.ClientSession | None = None

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: dict[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {"chat_id": chat_id, "text": text}
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup

        await self._request("sendMessage", payload)

    async def send_voice(
        self,
        chat_id: int,
        voice_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> None:
        form = aiohttp.FormData()
        form.add_field("chat_id", str(chat_id))
        form.add_field(
            "voice",
            voice_bytes,
            filename=filename,
            content_type=content_type,
        )
        await self._request_multipart("sendVoice", form)

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
    ) -> None:
        payload: dict[str, Any] = {"callback_query_id": callback_query_id}
        if text:
            payload["text"] = text

        await self._request("answerCallbackQuery", payload)

    async def broadcast(
        self,
        chat_ids: set[int],
        text: str,
        reply_markup: dict[str, Any] | None = None,
    ) -> None:
        for chat_id in chat_ids:
            try:
                await self.send_message(chat_id, text, reply_markup=reply_markup)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Failed to send Telegram message to chat_id=%s", chat_id)

    async def broadcast_voice(
        self,
        chat_ids: set[int],
        voice_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> None:
        for chat_id in chat_ids:
            try:
                await self.send_voice(chat_id, voice_bytes, filename, content_type)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Failed to send Telegram voice to chat_id=%s", chat_id)

    async def download_file(self, file_id: str) -> TelegramFile:
        session = await self._get_session()
        result = await self._request("getFile", {"file_id": file_id})
        file_path = result["file_path"]

        async with session.get(
            f"https://api.telegram.org/file/bot{self._token}/{file_path}",
            timeout=aiohttp.ClientTimeout(total=35),
        ) as response:
            response.raise_for_status()
            content = await response.read()

        return TelegramFile(content=content, file_path=file_path)

    async def poll_updates(
        self,
        allowed_chat_ids: set[int],
        on_message: MessageHandler | None = None,
        on_callback_query: CallbackHandler | None = None,
    ) -> None:
        await self._request("deleteWebhook", {"drop_pending_updates": False})
        offset = await self._skip_pending_updates()

        while True:
            try:
                updates = await self._request(
                    "getUpdates",
                    {
                        "offset": offset,
                        "timeout": 30,
                        "allowed_updates": ["message", "callback_query"],
                    },
                )

                for update in updates:
                    offset = update["update_id"] + 1
                    await self._handle_update(
                        update,
                        allowed_chat_ids,
                        on_message=on_message,
                        on_callback_query=on_callback_query,
                    )
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Telegram polling failed, retrying")
                await asyncio.sleep(5)

    async def _skip_pending_updates(self) -> int:
        updates = await self._request(
            "getUpdates",
            {"timeout": 0, "allowed_updates": ["message", "callback_query"]},
        )

        if not updates:
            return 0

        return updates[-1]["update_id"] + 1

    async def _handle_update(
        self,
        update: dict[str, Any],
        allowed_chat_ids: set[int],
        on_message: MessageHandler | None = None,
        on_callback_query: CallbackHandler | None = None,
    ) -> None:
        callback_query = update.get("callback_query") or {}
        if callback_query:
            message = callback_query.get("message") or {}
            chat = message.get("chat") or {}
            chat_id = chat.get("id")

            if not isinstance(chat_id, int) or chat_id not in allowed_chat_ids:
                return

            if on_callback_query is not None:
                await on_callback_query(callback_query)

            return

        message = update.get("message") or {}
        text = message.get("text", "")
        chat = message.get("chat") or {}
        chat_id = chat.get("id")

        if not isinstance(chat_id, int) or chat_id not in allowed_chat_ids:
            return

        if text.startswith("/start"):
            await self.send_message(chat_id, "Admin bot active")
            return

        if on_message is not None:
            await on_message(message)

    async def _request(self, method: str, payload: dict[str, Any]) -> Any:
        session = await self._get_session()

        async with session.post(
            f"{self._base_url}/{method}",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=35),
        ) as response:
            response.raise_for_status()
            data = await response.json()

        if not data.get("ok"):
            raise RuntimeError(f"Telegram API error on {method}: {data}")

        return data["result"]

    async def _request_multipart(self, method: str, form: aiohttp.FormData) -> Any:
        session = await self._get_session()

        async with session.post(
            f"{self._base_url}/{method}",
            data=form,
            timeout=aiohttp.ClientTimeout(total=35),
        ) as response:
            response.raise_for_status()
            data = await response.json()

        if not data.get("ok"):
            raise RuntimeError(f"Telegram API error on {method}: {data}")

        return data["result"]

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

        return self._session
