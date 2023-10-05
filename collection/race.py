from dataclasses import dataclass
import asyncio
import aiohttp
from constants import RACE_URL, URL_SUFFIX

@dataclass(slots=True)
class Race:
    id: str
    name: str
    description: str
    associated_champions: list[str]
    associated_stories: list[str]

def race_url(race: str):
    return f"{RACE_URL}/{race}/{URL_SUFFIX}"

async def get_race_info(session: aiohttp.ClientSession, r: str):
    print(f"\tGetting {r} race info...")
    async with session.get(race_url(r)) as response:
        json = await response.json()

        race_data = json['race']

        race = Race(
            id = json['id'],
            name = json['name'],
            description = race_data['overview']['short'],
            associated_champions = [c['slug'] for c in json['associated-champions']],
            associated_stories = [s['story-slug'] for s in json['modules'] if s['type'] == 'story-preview']
        )

        return race

async def get_races(session: aiohttp.ClientSession, races: list[str]) ->list[Race]:
    return await asyncio.gather(*[get_race_info(session, race) for race in races])
