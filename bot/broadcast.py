import asyncio
import aiohttp

MESSAGE = """
Начался эфир на тему - Расширенная Диагностика
"""
async def send_message(session: aiohttp.ClientSession, token: str, chat_id: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    reply_markup = {
        "inline_keyboard": [[{"text": "Подключиться", "url": "https://telemost.yandex.ru/j/27789817315254"}]]
    }
    async with session.post(url, json={"chat_id": chat_id, "text": MESSAGE, "reply_markup": reply_markup}) as resp:
        data = await resp.json()
        if data.get("ok"):
            print(f"[OK] {chat_id}")
        else:
            print(f"[FAIL] {chat_id}: {data.get('description')}")


async def main(token: str, chat_ids: list[str]) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = [send_message(session, token, cid) for cid in chat_ids]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    token = ""
    chat_ids = [
]
    asyncio.run(main(token, chat_ids))
