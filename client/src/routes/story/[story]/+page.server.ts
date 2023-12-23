import type { Story } from "$lib/documents";
import type { MLTResponse } from "$lib/query";
import { solrUrl } from "$lib/solr";
import type { PageServerLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ fetch, params }) => {
    const { story: storyId } = params;

    const mltParams = new URLSearchParams({
        "mlt.fl": "content, title, author, related_champions.name",
        "mlt.minwl": "3",
        "mlt.mindf": "1",
        "mlt.maxdf": "25",
        q: storyId,
        df: "id",
    });
    const mltUrl = solrUrl("mlt", mltParams);

    try {
        const response = await fetch(mltUrl, {
            method: "GET",
            headers: {
                Accept: "application/json",
            },
        });

        if (!response.ok) error(response.status, response.statusText);

        const data: MLTResponse<Story> = await response.json();

        const story = data.match.docs[0];
        const otherStories = data.response.docs;

        return {
            story,
            otherStories,
        };
    } catch (_e) {
        console.log(_e);
        error(500, "Failed to fetch results");
    }
};
