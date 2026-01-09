import asyncio
import aiohttp

from .champion import get_champions
from .constants import EXPLORE_URL, SEARCH_URL
from .region import get_regions
from .story import get_stories

import sys
sys.path.append("..")
from common.files import write_json_list
sys.path.pop()

async def get_champions_and_regions(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
    print("Getting champions and regions...")
    async with semaphore, session.get(SEARCH_URL) as response:
        json = await response.json()

        champions = json['champions']
        regions = json['factions']

        champions = [champion['slug'] for champion in champions]
        regions = [region['slug'] for region in regions]

        return champions, regions

async def get_story_names(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
    print("Getting story names...")
    async with semaphore, session.get(EXPLORE_URL) as response:
        json = await response.json()

        stories = json['modules']

        return [story['story-slug'] for story in stories if story['type'] == 'story-preview']

async def main():
    semaphore = asyncio.Semaphore(8)

    async with aiohttp.ClientSession() as session:
        champions, regions = await get_champions_and_regions(session, semaphore)
        champions = await get_champions(session, semaphore, champions)
        regions = await get_regions(session, semaphore, regions)

        stories = await get_story_names(session, semaphore)
        stories = await get_stories(session, semaphore, stories)

    write_json_list(champions, "champions", "collected")
    write_json_list(regions, "regions", "collected")
    write_json_list(stories, "stories", "collected")

if __name__ == '__main__':
    asyncio.run(main())
