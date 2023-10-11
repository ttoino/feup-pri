import asyncio
import glob
import math
from dataclasses import dataclass

import seaborn as sns

import matplotlib
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
def plot_champion_social_graph(connections):
    G = nx.DiGraph()
    G.add_edges_from(connections)

    size = 30
    plt.figure(figsize=(size,size))

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size = 50)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=False)

    plt.savefig("data/characterization/champion_social_graph.png")
    plt.clf()

def plot_data(data: dict, title, xlabel, ylabel, filename):
    plot = sns.lineplot(data)

    plot.set_title(title)
    plot.set_xlabel(xlabel)
    plot.set_ylabel(ylabel)

    plt.savefig(f"data/characterization/{filename}.png")
    plt.clf()

async def main():

    num_collections = len(glob.glob("data/collected/*"))

    stories = read_json_list("stories", "processed")

    stats: list[StoryStats] = []

    longest_story_word_count, longest_story_id = -math.inf, None
    shortest_story_word_count, shortest_story_id = math.inf, None
    total_word_count = 0
    total_read_time_minutes = 0

    stories_by_year = {}
    words_by_year = {}

    connections = []

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

        for champion in story["related_champions"]: 
            champion_connections = champion["related_champions"]

            for connection in champion_connections:
                connections.append((champion["name"], connection))

    num_stories = len(stories)
    average_word_count = total_word_count / num_stories
    story_words_by_year = {year: (words_by_year[year] / stories_by_year[year]) for year in stories_by_year.keys()}

    aggregated_stats = {
        'id': 'data',
        'num_collections': num_collections,
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

    plot_data(stories_by_year, "Stories by Year", "Year", "Number of Stories", "stories_by_year")
    plot_data(words_by_year, "Words by Year", "Year", "Number of Words", "words_by_year")
    plot_data(story_words_by_year, "Words per story per year", "Year","Number of words per story per year", "story_words_by_year" )
    
    print("Plotting champion social graph...")
    plot_champion_social_graph(connections)

if __name__ == '__main__':
    asyncio.run(main())