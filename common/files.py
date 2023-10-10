import dataclasses
import json
import os

def write_json_item(item, folder: str):
    with open(f"{folder}/{item['id'] if type(item) is dict else item.id}.json", 'w', encoding='utf-8') as file:
        json.dump(item if type(item) is dict else dataclasses.asdict(item), file, indent=4, ensure_ascii=False)

def write_json_list(data, data_type: str, category: str):
    folder_path = f'data/{category}/{data_type}'

    print(f"Writing {data_type} json data to '{folder_path}'...")
    os.makedirs(folder_path, exist_ok=True)

    for item in data:
        write_json_item(item, folder_path)

def read_json_list(data_type: str, category: str):
    folder_path = f'data/{category}/{data_type}'

    print(f"Loading {data_type} json data from '{folder_path}'...")
    data = []

    for file in os.listdir(folder_path):
        with open(f"{folder_path}/{file}", 'r', encoding='utf-8') as f:
            data.append(json.load(f))

    return data
