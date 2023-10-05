from dataclasses import dataclass
import asyncio
import aiohttp

@dataclass(slots=True)
class Region:
    id: str
    name: str
    description: str
    associated_champions: list[str]

async def get_region_info(session: aiohttp.ClientSession, region_url: str):
    async with session.get(region_url) as response:
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
