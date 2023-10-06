from dataclasses import dataclass
import asyncio
import aiohttp
from constants import CHAMPION_URL, URL_SUFFIX, WIKI_URL
from story import Story
from bs4 import BeautifulSoup

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
    races: list[str]

def champion_url(champion: str):
    return f"{CHAMPION_URL}/{champion}/{URL_SUFFIX}"

def champion_wiki_url(champion: str):
    return f"{WIKI_URL}/{champion}/LoL"

async def get_champion_info(session: aiohttp.ClientSession, c: str):
    print(f"\tGetting {c} champion info...")

    async with session.get(champion_url(c)) as response:
        json = await response.json()

        champion_data = json['champion']

        champion = Champion(
            id = json['id'],
            name = json['name'],
            title = json['title'],
            origin = champion_data['associated-faction-slug'],
            release_date = champion_data['release-date'],
            roles = [],
            skins = [],
            races = [race['slug'] for race in champion_data['races']],
            related_champions = [c['slug'] for c in json['related-champions']],
        )

    async with session.get(champion_wiki_url(c)) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        champion.roles = [role.text for role in soup.select('div[data-source="role"] a:last-child')]
        champion.skins = [skin.attrs['title'] for skin in soup.select('.skinviewer-show:not(:first-child) > span[title]')]

    return champion

async def get_champions(session: aiohttp.ClientSession, champions: list[str]) -> list[Champion]:
    return await asyncio.gather(*[get_champion_info(session, champion) for champion in champions])

