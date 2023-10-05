from champion import get_champions
from region import get_regions

import aiohttp
import asyncio

BASE_URL = "https://universe-meeps.leagueoflegends.com/v1"
SEARCH_URL = f"{BASE_URL}/en_us/search/index.json"
CHAMPION_URL = f"{BASE_URL}/en_us/champions/"
REGION_URL = f"{BASE_URL}/en_us/factions/"

async def get_champions_and_regions(session: aiohttp.ClientSession):
    async with session.get(SEARCH_URL) as response:
        json = await response.json()

        champions = json['champions']
        regions = json['factions']

        champions = [champion['url'].split('/')[-1] for champion in champions]
        regions = [region['url'].split('/')[-1] for region in regions]

        return champions, regions


async def main():
    async with aiohttp.ClientSession() as session:
        champions, regions = await get_champions_and_regions(session)
        champions = await get_champions(session, champions)
        regions = await get_regions(session, regions)

if __name__ == '__main__':
    asyncio.run(main())
