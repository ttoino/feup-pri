import { env } from "$env/dynamic/private";
import { SOLR_CORE } from "$env/static/private";
import type { Story } from "$lib/documents";
import type { GetResponse } from "$lib/query";
import type { PageServerLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ fetch, params }) => {
    const { story: storyId } = params;

    const solrUrl = env.SOLR_URL ?? "http://localhost:8983/solr";
    const getUrl = `${solrUrl}/${SOLR_CORE}/get?id=${encodeURIComponent(
        storyId,
    )}`;

    try {
        const response = await fetch(getUrl, {
            method: "GET",
            headers: {
                Accept: "application/json",
            },
        });

        if (!response.ok) throw error(response.status, response.statusText);

        const data: GetResponse<Story> = await response.json();

        const story = data.doc;

        return {
            story,
        };
    } catch (_e) {
        throw error(500, "Failed to fetch results");
    }
};
