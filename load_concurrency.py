import asyncio
import httpx

SUCCESS = 0
FAILED = 0


async def purchase():
    global SUCCESS, FAILED

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/purchase/1"
        )

        if response.status_code == 200:
            SUCCESS += 1
        else:
            FAILED += 1


async def main():
    tasks = []

    for _ in range(100):
        tasks.append(purchase())

    await asyncio.gather(*tasks)

    print(f"Successful purchases: {SUCCESS}")
    print(f"Failed purchases: {FAILED}")


asyncio.run(main())