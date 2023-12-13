export interface Story {
    id: string;
    title: string;
    author?: string;
    content: string;
    content_raw: string;
    date: string;
    image: string;
    related_champions: Champion[];
    type: "story";
    entities: string[];
    vector: number[];
}

export interface Champion {
    id: string;
    name: string;
    title: string;
    origin: Region;
    release_date: string;
    quote: string;
    icon: string;
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
