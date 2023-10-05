from dataclasses import dataclass
import asyncio
import aiohttp
from constants import REGION_URL, URL_SUFFIX

@dataclass(slots=True)
class Region:
    id: str
    name: str
    description: str
    associated_champions: list[str]

def region_url(region: str):
    return f"{REGION_URL}/{region}/{URL_SUFFIX}"

async def get_region_info(session: aiohttp.ClientSession, r: str):
    async with session.get(region_url(r)) as response:
        json = await response.json()

        region = Region(
            id = json['id'],
            name = json['faction']['name'],
            description = json['faction']['overview']['short'],
            associated_champions = [c['slug'] for c in json['associated-champions']]
        )

        return region

async def get_regions(session: aiohttp.ClientSession, regions: list[str]):
    return await asyncio.gather(*[get_region_info(session, region) for region in regions])
