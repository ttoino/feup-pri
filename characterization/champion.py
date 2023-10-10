from dataclasses import dataclass


dataclass(slots=True)
class Statistics:
    total: int

def read_champion_json():
    json_files = glob.glob('data/models/*.json')
