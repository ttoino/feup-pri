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
        sort: "{!func} product(tf(content,q),idf(content,q)) desc, score desc",
        params: {
            mm: "2",
            df: "content",
            "q.alt": "*",
            qs: "1",
            ps: "3",
            indent: "true",
            fl: "*,score",
            "q.op": "OR",
            tie: "0.1",
            defType: "edismax",
            qf: "content^5 title^3 related_champions.name^1.5 related_champions.title^1.5 related_champions.aliases^1.7 entities^2 author",
            pf: "content^3",
            pf3: "content^3",
            pf2: "content^3",
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

        let profile = null;
        if (query + "-bio" == results[0].id){
            profile = {
                id: results[0]["related_champions.id"][0],
                name: results[0]["related_champions.name"][0],
                title: results[0]["related_champions.title"][0],
                image: results[0]["related_champions.image"][0],
                content: results[0].content
            }
        }

        return {
            results,
            query: url.searchParams.get("query"),
            current: parseInt(page),
            pages: maxPage,
            profile
        };
    } catch (_e) {
        throw error(500, "Failed to fetch results");
    }
};
