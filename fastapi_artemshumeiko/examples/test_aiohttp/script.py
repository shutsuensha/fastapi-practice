import asyncio
import aiohttp


async def get_data(i: int, endpoint: str):
    print(f'Start {i}')
    url = f'http://127.0.0.1:8000/{endpoint}/{i}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f'End {i}')


async def main():
    await asyncio.gather(*[get_data(i, 'sync') for i in range(300)])


asyncio.run(main())