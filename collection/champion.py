import asyncio
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup
from .constants import CHAMPION_URL, URL_SUFFIX, WIKI_URL
from .util import raw_text

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
    icon: str
    image: str
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
            biography_raw = raw_text(biography_data['full']),
            release_date = champion_data['release-date'],
            icon = '',
            image = champion_data['image']['uri'],
            roles = [],
            skins = [],
            races = [],
            aliases = [],
            related_champions = [c['name'] for c in json['related-champions']],
        )

    async with session.get(champion_wiki_url(champion.name.replace("’", "'"))) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        champion.races = list({race.text.strip() for race in soup.select('div[data-source="species"] li, div[data-source="species"] > :last-child:not(:has(li))') if race.select_one('s') is None})
        champion.aliases = list({alias.text.strip() for alias in soup.select('div[data-source="alias"] li, div[data-source="alias"] > :last-child:not(:has(li))')})

    async with session.get(champion_wiki_lol_url(champion.name.replace("’", "'"))) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        champion.roles = list({role.text.strip() for role in soup.select('div[data-source="role"] a:last-child')})
        champion.skins = list({skin.attrs['title'].strip() for skin in soup.select('.skinviewer-show:not(:first-child) > span[title]')})
        icon = soup.select_one('.skinviewer-show:first-child > span[title] > img')
        if icon:
            champion.icon = icon.attrs['data-src']

    return champion

async def get_champions(session: aiohttp.ClientSession, champions: list[str]) -> list[Champion]:
    return await asyncio.gather(*[get_champion_info(session, champion) for champion in champions])

