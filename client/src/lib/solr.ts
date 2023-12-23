import { env } from "$env/dynamic/private";

export const solrUrl = (path: string, params = new URLSearchParams()) => {
    const solrUrl = env.SOLR_URL ?? "http://localhost:8983/solr";
    const solrCore = env.SOLR_CORE ?? "luis";
    return `${solrUrl}/${solrCore}/${path}?${params.toString()}`;
};
