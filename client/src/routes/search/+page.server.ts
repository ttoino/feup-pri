import { env } from "$env/dynamic/private";
import { SOLR_CORE } from "$env/static/private";
import type { Champion, Story } from "$lib/documents";
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
            spellcheck: "true",
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

        console.log(data);

        const results = data.response.docs;
        const maxPage = Math.ceil(data.response.numFound / limit);

        let profile: Champion | null = null;

        for (let i = 0; i < results.length; i++) {
            if (
                query.toLowerCase().replaceAll(/[^a-z]/g, "") + "-bio" ==
                results[i].id
            ) {
                console.log(results[0]);
                profile = {
                    id: results[i]["related_champions.id"][0],
                    name: results[i]["related_champions.name"][0],
                    title: results[i]["related_champions.title"][0],
                    release_date:
                        results[i]["related_champions.release_date"][0],
                    quote: results[i]["related_champions.quote"][0],
                    image: results[i]["related_champions.image"][0],
                    roles: results[i]["related_champions.roles"],
                    skins: results[i]["related_champions.skins"],
                    races: results[i]["related_champions.races"],
                    aliases: results[i]["related_champions.aliases"],
                    related_champions:
                        results[i]["related_champions.related_champions"],
                    type: "champion",
                };

                if (results[i]["related_champions.origin.id"])
                    profile.origin = {
                        id: results[i]["related_champions.origin.id"][0],
                        name: results[i]["related_champions.origin.name"][0],
                        description:
                            results[i][
                                "related_champions.origin.description"
                            ][0],
                        description_raw:
                            results[i][
                                "related_champions.origin.description_raw"
                            ][0],
                        image: results[i]["related_champions.origin.image"][0],
                        associated_champions:
                            results[i][
                                "related_champions.origin.associated_champions"
                            ],
                        type: "region",
                    };

                results.splice(i, 1);
                break;
            }
        }

        const spellcheck = data.spellcheck?.collations
            .filter((_, i) => i % 2 === 1)
            .map((s) => s.toLowerCase());

        return {
            results,
            query: url.searchParams.get("query"),
            current: parseInt(page),
            pages: maxPage,
            profile,
            spellcheck,
        };
    } catch (_e) {
        console.error(_e);
        throw error(500, "Failed to fetch results");
    }
};
