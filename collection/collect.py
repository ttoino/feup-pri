import asyncio
import dataclasses
import json
import os

import aiohttp
from champion import get_champions
from constants import EXPLORE_URL, SEARCH_URL
from race import get_races
from region import get_regions
from story import get_stories


def write_json_item(item, folder):
    with open(f"{folder}/{item.id}.json", 'w', encoding='utf-8') as file:
        json.dump(dataclasses.asdict(item), file, indent=4, ensure_ascii=False)


def write_json_list(data, data_type, category):

    folder_path = f'data/{category}/{data_type}'

    print(f"Writing {data_type} json data to '{folder_path}'...")
    os.makedirs(folder_path, exist_ok=True)

    for item in data:
        write_json_item(item, folder_path)

async def get_champions_and_regions(session: aiohttp.ClientSession):
    print("Getting champions and regions...")
    async with session.get(SEARCH_URL) as response:
        json = await response.json()

        champions = json['champions']
        regions = json['factions']

        champions = [champion['slug'] for champion in champions]
        regions = [region['slug'] for region in regions]

        return champions, regions

async def get_story_names(session: aiohttp.ClientSession):
    print("Getting story names...")
    async with session.get(EXPLORE_URL) as response:
        json = await response.json()

        stories = json['modules']

        return [story['story-slug'] for story in stories if story['type'] == 'story-preview']

async def main():
    async with aiohttp.ClientSession() as session:
        champions, regions = await get_champions_and_regions(session)
        champions = await get_champions(session, champions)
        regions = await get_regions(session, regions)

        races = list({r for c in champions for r in c.races})
        races = await get_races(session, races)

        stories = await get_story_names(session)
        stories = await get_stories(session, stories)

    write_json_list(champions, "champions", "models")
    write_json_list(regions, "regions", "models")
    write_json_list(stories, "stories", "models")
    write_json_list(races, "races", "models")

if __name__ == '__main__':
    asyncio.run(main())
