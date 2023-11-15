import sys
sys.path.append("..")
from common.files import read_json_list
sys.path = sys.path[:-2]

import json

def main():
    stories = read_json_list("stories", "processed")

    for story in stories:
        for champion in story['related_champions']:
            
            champion['name_txt'] = champion['name']
            del champion['name']

            champion['title_txt'] = champion['title']
            del champion['title']

            if champion['origin']:
                champion['origin']['name_txt'] = champion['origin']['name']
                del champion['origin']['name']

                champion['origin']['description_txt'] = champion['origin']['description']
                del champion['origin']['description']

                champion['origin']['description_raw_txt'] = champion['origin']['description_raw']
                del champion['origin']['description_raw']

                champion['origin']['image_s'] = champion['origin']['image']
                del champion['origin']['image']

                champion['origin']['associated_champions_ss'] = champion['origin']['associated_champions']
                del champion['origin']['associated_champions']

            champion['release_date_dt'] = champion['release_date']
            del champion['release_date']

            champion['quote_txt'] = champion['quote']
            del champion['quote']

            champion['icon_s'] = champion['icon']
            del champion['icon']

            champion['image_s'] = champion['image']
            del champion['image']

            champion['roles_ss'] = champion['roles']
            del champion['roles']

            champion['skins_ss'] = champion['skins']
            del champion['skins']

            champion['races_ss'] = champion['races']
            del champion['races']

            champion['related_champions_ss'] = champion['related_champions']
            del champion['related_champions']

            champion['aliases_ss'] = champion['aliases']
            del champion['aliases']

            champion['type_s'] = champion['type']
            del champion['type']


    with open("solr/data.json", "w", encoding="utf8") as f:
        json.dump(stories, f, indent=4, ensure_ascii=True)

if __name__ == '__main__':
    main()