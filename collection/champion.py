import asyncio
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup
from .constants import CHAMPION_URL, URL_SUFFIX, WIKI_URL

@dataclass(slots=True)
class Champion:
    id: str
    name: str
    title: str
    origin: str
    release_date: str
    quote: str
    biography: str
    biography_raw: str
    roles: list[str]
    skins: list[str]
    races: list[str]
    aliases: list[str]
    related_champions: list[str]

def champion_url(champion: str):
    return f"{CHAMPION_URL}/{champion}/{URL_SUFFIX}"

def champion_wiki_url(champion: str):
    return f"{WIKI_URL}/{champion}"

def champion_wiki_lol_url(champion: str):
    return f"{WIKI_URL}/{champion}/LoL"

async def get_champion_info(session: aiohttp.ClientSession, c: str):
    print(f"\tGetting {c} champion info...")

    async with session.get(champion_url(c)) as response:
        json = await response.json()

        champion_data = json['champion']

        biography_data = champion_data['biography']

        champion = Champion(
            id = json['id'],
            name = json['name'],
            title = json['title'],
            origin = champion_data['associated-faction-slug'],
            quote = biography_data['quote'],
            biography = biography_data['full'],
            biography_raw = BeautifulSoup(biography_data['full'], 'html.parser').get_text(),
            release_date = champion_data['release-date'],
            roles = [],
            skins = [],
            races = [],
            aliases = [],
            related_champions = [c['name'] for c in json['related-champions']],
        )

    async with session.get(champion_wiki_url(c)) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        champion.races = [race.text for race in soup.select('div[data-source="species"] li') if race.select_one('s') is None]
        champion.aliases = [alias.text for alias in soup.select('div[data-source="alias"] li')]

    async with session.get(champion_wiki_lol_url(c)) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        champion.roles = [role.text for role in soup.select('div[data-source="role"] a:last-child')]
        champion.skins = [skin.attrs['title'] for skin in soup.select('.skinviewer-show:not(:first-child) > span[title]')]

    return champion

async def get_champions(session: aiohttp.ClientSession, champions: list[str]) -> list[Champion]:
    return await asyncio.gather(*[get_champion_info(session, champion) for champion in champions])

