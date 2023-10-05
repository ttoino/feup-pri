from champion import get_champions
from region import get_regions
from story import get_stories
from constants import SEARCH_URL, EXPLORE_URL
import json
import os

import aiohttp
import asyncio

async def get_champions_and_regions(session: aiohttp.ClientSession):
    async with session.get(SEARCH_URL) as response:
        json = await response.json()

        champions = json['champions']
        regions = json['factions']

        champions = [champion['slug'] for champion in champions]
        regions = [region['slug'] for region in regions]

        return champions, regions

async def get_story_names(session: aiohttp.ClientSession):
    async with session.get(EXPLORE_URL) as response:
        json = await response.json()

        stories = json['modules']

        return [story['story-slug'] for story in stories]

def write_json(data, folder):
    os.makedirs(folder, exist_ok=True)

    for item in data:
        with open(f"data/{folder}/{item['id']}.json", 'w', encoding='utf-8') as file:
            json.dump(item, file, indent=4, ensure_ascii=False)

async def main():
    async with aiohttp.ClientSession() as session:
        champions, regions = await get_champions_and_regions(session)
        champions = await get_champions(session, champions)
        regions = await get_regions(session, regions)

        stories = await get_story_names(session)
        stories = await get_stories(session, stories)
    
    write_json(champions, "champions")
    write_json(regions, "regions")
    write_json(stories, "stories")

if __name__ == '__main__':
    asyncio.run(main())
