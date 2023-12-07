import en_core_web_lg
from sentence_transformers import SentenceTransformer

import sys
sys.path.append("..")
from common.files import read_json_list, write_json_list
sys.path = sys.path[:-2]

def extract_biographies(champions):
    stories = []

    for champion in champions:
        stories.append({
            'id': champion['id'] + '-bio',
            'title': champion['name'],
            'author': None,
            'content': champion['biography'],
            'content_raw': champion['biography_raw'],
            'date': champion['release_date'],
            'image': champion['image'],
            'related_champions': [champion['id']],
        })

        del champion['biography']
        del champion['biography_raw']

    return stories

def join_champions_and_region(champions, regions):
    regions = {region['id']: {**region, 'type': 'region'} for region in regions}

    for champion in champions:
        champion['origin'] = None if champion['origin'] == 'unaffiliated' else regions[champion['origin']]

def join_stories_and_champions(stories, champions):
    championsMap = {champion['id']: {**champion, 'type': 'champion'} for champion in champions}

    for story in stories:
        story['related_champions'] = [championsMap[c] for c in story['related_champions']]

def nlp(stories):
    nlp = en_core_web_lg.load()

    for story in stories:
        doc = nlp(story['content_raw'])

        story['entities'] = list({entity.text for entity in doc.ents if entity.label_ not in ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']})

def add_vector(stories):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    for story in stories:
        content = story['title'] + ' ' + story['content_raw']
        story['vector'] = model.encode(content, convert_to_tensor=False).tolist()

def main():
    champions = read_json_list("champions", "collected")
    regions = read_json_list("regions", "collected")
    stories = read_json_list("stories", "collected")

    stories += extract_biographies(champions)

    for story in stories:
        story['type'] = 'story'

    join_champions_and_region(champions, regions)
    join_stories_and_champions(stories, champions)

    try:
        add_vector(stories)
    except:
        print("Could not add vector to stories.")
    
    nlp(stories)

    write_json_list(stories, "stories", "processed")

if __name__ == '__main__':
    main()
