import asyncio
from dataclasses import dataclass
import traceback

import aiohttp
from .constants import STORY_URL, URL_SUFFIX
from .util import raw_text


@dataclass(slots=True)
class Story:
    id: str
    title: str
    author: str | None
    content: str
    content_raw: str    
    date: str
    image: str
    related_champions: list[str]

def story_url(story: str):
    return f"{STORY_URL}/{story}/{URL_SUFFIX}"

async def get_story_info(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, s: str):
    print(f"\tGetting {s} story info...")

    try:
        async with semaphore, session.get(story_url(s)) as response:
            json = await response.json()

        author = json['story']['subtitle']
        if author.lower().startswith('by '):
            author = author[3:]
        else:
            author = None

        image = json['story']['story-sections'][0]['background-image']
        if image is not None:
            image = image['uri']

        content = ""
        related_champions = set()

        for section in json['story']['story-sections']:
            for subsection in section['story-subsections']:
                content += subsection['content'] or ""

            related_champions |= {c['slug'] for c in section['featured-champions']}

        story = Story(
            id = json['id'],
            title = json['story']['title'],
            author = author,
            content = content,
            content_raw = raw_text(content),
            date = json['release-date'],
            image = image,
            related_champions = list(related_champions),
        )
    except Exception:
        print(f"Error getting {s} story info:\n{traceback.format_exc()}")
        raise

    return story
    
async def get_stories(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, stories: list[str]):
    return await asyncio.gather(*[get_story_info(session, semaphore, story) for story in stories])
