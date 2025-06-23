import asyncio
import websockets
import json
import re

KEYWORDS = ["telegram", "teleg", "-tg", "telep"]

async def listen():
    url = "ws://localhost:8080/domains-only"
    async with websockets.connect(url) as ws:
        async for message in ws:
            data = json.loads(message)
            for domain in data.get("data", []):  # domains-only stream returns a list
                if any(re.search(keyword, domain, re.IGNORECASE) for keyword in KEYWORDS):
                    print(f"[FOUND] {domain}")

asyncio.run(listen())
