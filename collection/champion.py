from dataclasses import dataclass
import asyncio
import aiohttp

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

async def get_champion_info(session: aiohttp.ClientSession, champion_url: str):
    async with session.get(champion_url) as response:
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

