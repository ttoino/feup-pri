import asyncio
import glob
import math
from dataclasses import dataclass
from PIL import Image
import requests
import io
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np

import seaborn as sns

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import networkx as nx

import os

from dateutil.parser import isoparse

from common.files import read_json_list, write_json_item

AVG_READ_TIME = 200 # words per minute

@dataclass(slots=True, frozen=True)
class StoryStats:
    num_words: int
    num_related_champions: int
    read_time_minutes: float

def process_story(story: dict) -> StoryStats:
    num_words = len(story["content_raw"].split())
    num_related_champions = len(story["related_champions"])
    read_time_minutes = num_words / AVG_READ_TIME

    return StoryStats(num_words, num_related_champions, read_time_minutes)

# https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
def plot_champion_social_graph(champions):
    connections = [(c['name'], oc) for c in champions for oc in c['related_champions']]
    champions = {c['name']: c['icon'] for c in champions}

    G = nx.DiGraph()
    G.add_edges_from(connections)

    fig, ax = plt.subplots()

    size = 15
    fig.set_size_inches(size, size)
    fig.subplots_adjust(0, 0, 1, 1, 0, 0)

    tr_figure = ax.transData.transform
    tr_axes = fig.transFigure.inverted().transform

    icon_size = 0.025
    icon_center = icon_size / 2.0

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    pos = nx.nx_agraph.graphviz_layout(G, prog='fdp')
    nx.draw_networkx_edges(G, pos, arrows=False)
    for n in G.nodes:
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))
        # get overlapped axes and plot icon
        a: Axes = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
        response = requests.get(chzampions[n])
        b = io.BytesIO(response.content)
        image = Image.open(b)
        a.imshow(image)
        a.axis("off")

    plt.savefig("data/characterization/champion_social_graph.png", dpi=800, transparent=True)
    plt.clf()

def plot_data(data: dict, title, xlabel, ylabel, filename):
    plot = sns.lineplot(data)

    plot.set_title(title)
    plot.set_xlabel(xlabel)
    plot.set_ylabel(ylabel)

    plt.savefig(f"data/characterization/{filename}.png", dpi=800, transparent=True)
    plt.clf()

def wordcloud(text: str, filename: str):
    logo = np.array(Image.open("characterization/logo.png"))

    wordcloud = WordCloud(
        background_color="#FFFFFFFF",
        stopwords=STOPWORDS | {'s'},
        mask=logo,
        mode="RGBA",
        random_state=42,
    )
    wordcloud.generate(text)
    colors = ImageColorGenerator(logo)

    fg = plt.figure(figsize=(10, 10))
    fg.subplots_adjust(0, 0, 1, 1, 0, 0)
    plt.imshow(wordcloud.recolor(color_func=colors), interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f"data/characterization/{filename}.png", dpi=800, transparent=True)
    plt.clf()

async def main():
    num_collections = len(glob.glob("data/collected/*"))

    stories = read_json_list("stories", "processed")
    champions = read_json_list("champions", "collected")

    stats: list[StoryStats] = []

    longest_story_word_count, longest_story_id = -math.inf, None
    shortest_story_word_count, shortest_story_id = math.inf, None
    total_word_count = 0
    total_read_time_minutes = 0

    stories_by_year = {}
    words_by_year = {}

    text = ""

    for story in stories:
        print(f"Processing {story['id']}...")

        story_stats = process_story(story)

        if story_stats.num_words > longest_story_word_count:
            longest_story_word_count = story_stats.num_words
            longest_story_id = story["id"]

        if story_stats.num_words < shortest_story_word_count:
            shortest_story_word_count = story_stats.num_words
            shortest_story_id = story["id"]

        total_word_count += story_stats.num_words
        total_read_time_minutes += story_stats.read_time_minutes

        if story['date']:
            story_year = isoparse(story["date"]).year
            stories_by_year[story_year] = stories_by_year.get(story_year, 0) + 1
            words_by_year[story_year] = words_by_year.get(story_year, 0) + story_stats.num_words

        stats.append(story_stats)

        text += '\n' + story['title'] + '\n' + story['content_raw']

    text.replace("’", "'")

    num_stories = len(stories)
    num_champions = len(champions)
    average_word_count = total_word_count / num_stories
    story_words_by_year = {year: (words_by_year[year] / stories_by_year[year]) for year in stories_by_year}

    aggregated_stats = {
        'id': 'data',
        'num_collections': num_collections,
        'num_champions': num_champions,
        'num_stories': num_stories,
        'total_word_count': total_word_count,
        'average_word_count': average_word_count,
        'longest_story': {
            'id': longest_story_id,
            'word_count': longest_story_word_count
        },
        'shortest_story': {
            'id': shortest_story_id,
            'word_count': shortest_story_word_count
        },
        'total_read_time_minutes': total_read_time_minutes,
        'stories_by_year': dict(sorted(stories_by_year.items())),
        'words_by_year': dict(sorted(words_by_year.items())),
    }

    os.makedirs("data/characterization", exist_ok=True)
    write_json_item(aggregated_stats, "data/characterization")

    wordcloud(text, "wordcloud")

    plot_data(stories_by_year, "Stories by Year", "Year", "Number of Stories", "stories_by_year")
    plot_data(words_by_year, "Words by Year", "Year", "Number of Words", "words_by_year")
    plot_data(story_words_by_year, "Avg. words per story by year", "Year", "Avg. number of words per story", "story_words_by_year" )
    
    print("Plotting champion social graph...")
    plot_champion_social_graph(champions)

if __name__ == '__main__':
    asyncio.run(main())