from dataclasses import dataclass
import asyncio
import aiohttp
from constants import CHAMPION_URL, URL_SUFFIX

@dataclass(slots=True)
class Champion:
    id: str
    name: str
    title: str
    origin: str
    release_date: str
    roles: list[str]
    skins: list[str]
    related_champions: list[str]

def champion_url(champion: str):
    return f"{CHAMPION_URL}/{champion}/{URL_SUFFIX}"

async def get_champion_info(session: aiohttp.ClientSession, c: str):
    print(f"\tGetting {c} champion info...")
    async with session.get(champion_url(c)) as response:
        json = await response.json()

        champion = Champion(
            id = json['id'],
            name = json['name'],
            title = json['title'],
            origin = json['champion']['associated-faction-slug'],
            release_date = json['champion']['release-date'],
            roles = [],
            skins = [],
            related_champions = [c['slug'] for c in json['related-champions']]
        )

        # TODO: skins, roles, stats, abilities from wiki

        return champion

async def get_champions(session: aiohttp.ClientSession, champions: list[str]):
    return await asyncio.gather(*[get_champion_info(session, champion) for champion in champions])

