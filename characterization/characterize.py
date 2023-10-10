import glob
from dataclasses import dataclass

import pandas as pd
import asyncio


class CollectionStatistics:
    num_files: int

@dataclass(slots=True)
class Statistics:
    collections: int
    collections_statistics: dict[str, CollectionStatistics]

async def read_collection(collection_path):

    json_files = glob.glob(f'{collection_path}/*')

    num_files = len(json_files)

    async def async_read_json(f):
        # Do this to have tasks created
        return pd.read_json(f)

    awaitable_read_files = [asyncio.create_task(async_read_json(f)) for f in json_files]

    read_files = await asyncio.gather(*awaitable_read_files)

    df = pd.concat(read_files)

    return CollectionStatistics(
        num_files=num_files
    ), df

async def read_collections():

    collections = glob.glob('data/models/*')

    num_collections = len(collections)
    print(f'Found {num_collections} collections')

    collections_statistics = {}
    dataframes = {}

    for f in collections:
        collection_name = f.split('/')[-1]

        print(f'Reading {collection_name} collection')
        stats, df = await read_collection(f)

        collections_statistics[collection_name] = stats
        dataframes[collection_name] = df

    return Statistics(
        collections=num_collections,
        collections_statistics=collections_statistics
    ), dataframes

async def main():
    stats, dfs = await read_collections();

    print(stats)

if __name__ == '__main__':
    asyncio.run(main())