#!/usr/bin/env python3

import json
from pathlib import Path


def main() -> None:
    source_path = Path(__file__).with_name("result.json")

    with source_path.open(encoding="utf-8") as source_file:
        records = json.load(source_file)

    chat_ids = [item["chat_id"] for item in records if item.get("chat_id") is not None]
    print(json.dumps(chat_ids, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
