import { env } from "$env/dynamic/private";
import { SOLR_CORE } from "$env/static/private";
import type { Story } from "$lib/documents";
import type { QueryRequest, QueryResponse } from "$lib/query";
import type { PageServerLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ url, fetch }) => {
    const query = url.searchParams.get("query") || "*:*";
    const page = url.searchParams.get("page") || "1";

    const solrUrl = env.SOLR_URL ?? "http://localhost:8983/solr";
    const searchUrl = `${solrUrl}/${SOLR_CORE}/query`;

    const limit = 20;
    const offset = (parseInt(page) - 1) * limit;

    const searchBody: QueryRequest = {
        query,
        offset,
        limit,
        sort: "score desc",
        params: {
            df: "content",
        },
    };

    try {
        const response = await fetch(searchUrl, {
            body: JSON.stringify(searchBody),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });
        const data: QueryResponse<Story> = await response.json();

        const results = data.response.docs;
        const maxPage = Math.ceil(data.response.numFound / limit);

        return {
            results,
            query: url.searchParams.get("query"),
            current: parseInt(page),
            pages: maxPage,
        };
    } catch (_e) {
        throw error(500, "Failed to fetch results");
    }
};
