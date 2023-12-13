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

    const mltBody = {
        "mlt.fl": "vector",
        "q": `id:${storyId}`
    };
    const mltParams = new URLSearchParams(mltBody);
    const mltUrl = `${solrUrl}/${SOLR_CORE}/mlt?${mltParams}` ;

    try {
        const response = await fetch(getUrl, {
            method: "GET",
            headers: {
                Accept: "application/json",
            },
        });

        const mltResponse = await fetch(mltUrl, {
            method: "GET",
            headers: {
                Accept: "application/json",
            },
        })

        if (!response.ok) throw error(response.status, response.statusText);
        if (!mltResponse.ok) throw error(mltResponse.status, mltResponse.statusText);

        const data: GetResponse<Story> = await response.json();
        const mltData = await mltResponse.json();

        const story = data.doc;
        const otherStories = mltData.response.docs;

        return {
            story, otherStories
        };
    } catch (_e) {
        console.log(_e)
        throw error(500, "Failed to fetch results");
    }
};
