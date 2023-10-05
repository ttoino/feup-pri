from dataclasses import dataclass
import asyncio
import aiohttp
from constants import STORY_URL, URL_SUFFIX

@dataclass(slots=True)
class Story:
    id: str
    title: str
    author: str | None
    content: str
    date: str
    type: str
    related_champions: list[str]
    related_regions: list[str]

def story_url(story: str):
    return f"{STORY_URL}/{story}/{URL_SUFFIX}"

async def get_story_info(session: aiohttp.ClientSession, s: str):
    async with session.get(story_url(s)) as response:
        json = await response.json()

        author = json['story']['subtitle']
        if author.lower().startswith('by '):
            author = author[3:]
        else:
            author = None

        content = ""
        related_champions = []
        related_regions = []

        for section in json['story']['story-sections']:
            for subsection in section['story-subsections']:
                content += subsection['content'] or ""
            
            related_champions += [c['slug'] for c in section['featured-champions']]
            # related_regions += [r['slug'] for r in section['featured-factions']]

        story = Story(
            id = json['id'],
            title = json['story']['title'],
            author = author,
            content = content,
            date = json['release-date'],
            type = json['type'],
            related_champions = related_champions,
            related_regions = related_regions
        )

        return story
    
async def get_stories(session: aiohttp.ClientSession, stories: list[str]):
    return await asyncio.gather(*[get_story_info(session, story) for story in stories])
