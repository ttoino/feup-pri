export interface Story {
    id: string;
    title: string;
    author?: string;
    content: string;
    content_raw: string;
    date: string;
    image: string;
    "related_champions.id": string[];
    "related_champions.name": string[];
    "related_champions.title": string[];
    "related_champions.release_date": string[];
    "related_champions.quote": string[];
    "related_champions.image": string[];
    "related_champions.roles": string[];
    "related_champions.skins": string[];
    "related_champions.races": string[];
    "related_champions.aliases": string[];
    "related_champions.related_champions": string[];
    "related_champions.type": "champion"[];
    "related_champions.origin.id": string[];
    "related_champions.origin.name": string[];
    "related_champions.origin.description": string[];
    "related_champions.origin.description_raw": string[];
    "related_champions.origin.image": string[];
    "related_champions.origin.associated_champions": string[];
    "related_champions.origin.type": "region"[];
    type: "story";
    entities: string[];
    vector: number[];
}

export interface Champion {
    id: string;
    name: string;
    title: string;
    origin?: Region;
    release_date: string;
    quote: string;
    image: string;
    roles: string[];
    skins: string[];
    races: string[];
    aliases: string[];
    related_champions: string[];
    type: "champion";
}

export interface Region {
    id: string;
    name: string;
    description: string;
    description_raw: string;
    image: string;
    associated_champions: string[];
    type: "region";
}
