import { env } from "$env/dynamic/private";
import { SOLR_CORE } from "$env/static/private";
import type { Story } from "$lib/documents";
import type { MLTResponse } from "$lib/query";
import type { PageServerLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ fetch, params }) => {
    const { story: storyId } = params;

    const solrUrl = env.SOLR_URL ?? "http://localhost:8983/solr";

    const mltBody = {
        "mlt.fl": "content, title, author, related_champions.name",
        q: storyId,
        df: "id",
    };
    const mltParams = new URLSearchParams(mltBody);
    const mltUrl = `${solrUrl}/${SOLR_CORE}/mlt?${mltParams}`;

    try {
        const response = await fetch(mltUrl, {
            method: "GET",
            headers: {
                Accept: "application/json",
            },
        });

        if (!response.ok) throw error(response.status, response.statusText);

        const data: MLTResponse<Story> = await response.json();

        const story = data.match.docs[0];
        const otherStories = data.response.docs;

        return {
            story,
            otherStories,
        };
    } catch (_e) {
        console.log(_e);
        throw error(500, "Failed to fetch results");
    }
};
