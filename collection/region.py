import asyncio
from dataclasses import dataclass
import aiohttp
import traceback

from .constants import REGION_URL, URL_SUFFIX
from .util import raw_text

@dataclass(slots=True)
class Region:
    id: str
    name: str
    description: str
    description_raw: str
    image: str
    associated_champions: list[str]

def region_url(region: str):
    return f"{REGION_URL}/{region}/{URL_SUFFIX}"

async def get_region_info(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, r: str):
    try:
        async with semaphore, session.get(region_url(r)) as response:
            print(f"\tGetting {r} region info...")
            json = await response.json()

        region = Region(
            id = json['id'],
            name = json['faction']['name'],
            description = json['faction']['overview']['short'],
            description_raw = raw_text(json['faction']['overview']['short']),
            image = json['faction']['image']['uri'],
            associated_champions = [c['name'] for c in json['associated-champions']]
        )
    except Exception:
        print(f"Error getting {r} region info:\n{traceback.format_exc()}")
        raise

    return region

async def get_regions(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, regions: list[str]):
    return await asyncio.gather(*[get_region_info(session, semaphore, region) for region in regions])
