import asyncio
from dataclasses import dataclass
import traceback

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
    return f"{WIKI_URL}/Universe:{champion}"

def champion_wiki_lol_url(champion: str):
    return f"{WIKI_URL}/{champion}"

async def get_champion_info(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, c: str):
    try:
        async with semaphore, session.get(champion_url(c)) as response:
            print(f"\tGetting {c} champion info...")
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

        async with semaphore, session.get(champion_wiki_url(champion.name.replace("’", "'"))) as response:
            print(f"\tGetting {c} champion wiki info...")
            html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')

        champion.races = list({race.text.strip() for race in soup.select('.infobox-data-label:-soup-contains(Species) ~ :is(.infobox-data-value li:not(:has(s)), .infobox-data-value:not(:has(li)))')})
        champion.aliases = list({alias.text.strip() for alias in soup.select('.infobox-data-label:-soup-contains(Alias) ~ :is(.infobox-data-value li:not(:has(s)), .infobox-data-value:not(:has(li)))')})

        async with semaphore, session.get(champion_wiki_lol_url(champion.name.replace("’", "'"))) as response:
            print(f"\tGetting {c} champion wiki lol info...")
            html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')

        champion.roles = list({role.text.strip() for role in soup.select('.infobox-data-label:-soup-contains(Class) ~ .infobox-data-value')})
        champion.skins = list({skin.attrs['title'].strip() for skin in soup.select('.skinviewer-show:not(:first-child) > span[title]')})
        champion.icon = soup.select_one('.skinviewer-show:first-child img').attrs['src']

    except Exception:
        print(f"\tError getting {c} champion info:\n{traceback.format_exc()}")
        raise

    return champion

async def get_champions(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, champions: list[str]) -> list[Champion]:
    return await asyncio.gather(*[get_champion_info(session, semaphore, champion) for champion in champions])

