import { env } from "$env/dynamic/private";
import type { Champion, Story } from "$lib/documents";
import type { QueryResponse } from "$lib/query";
import type { PageServerLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ url, fetch }) => {
    const query = url.searchParams.get("query") || "*:*";
    const page = url.searchParams.get("page") || "1";

    const solrUrl = env.SOLR_URL ?? "http://localhost:8983/solr";
    const solrCore = env.SOLR_CORE ?? "luis";
    const searchUrl = `${solrUrl}/${solrCore}/select`;

    const limit = 20;
    const offset = (parseInt(page) - 1) * limit;

    const urlParams = new URLSearchParams();
    urlParams.set("q", query);
    urlParams.set("rows", limit.toString());
    urlParams.set("start", offset.toString());
    urlParams.set("sort", "score desc");
    urlParams.set("defType", "edismax");
    urlParams.set("qf", "content^5 title^0.1 author");
    urlParams.set("pf", "content^3");
    urlParams.set("pf3", "content^3");
    urlParams.set("pf2", "content^3");
    urlParams.set("mm", "2");
    urlParams.set("df", "content");
    urlParams.set("q.alt", "*");
    urlParams.set("ps", "3");
    urlParams.set("qs", "1");
    urlParams.set("indent", "true");
    urlParams.set("fl", "*,score");
    urlParams.set("q.op", "OR");
    urlParams.set("tie", "0.1");
    urlParams.set("spellcheck", "true");

    try {
        const response = await fetch(`${searchUrl}?${urlParams.toString()}`, {
            headers: {
                Accept: "application/json",
            },
        });
        const data: QueryResponse<Story> = await response.json();

        console.log(data);

        const results = data.response.docs;
        const maxPage = Math.ceil(data.response.numFound / limit);

        let profile: (Champion & { content: string }) | null = null;

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

                    content: results[i].content,
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
        error(500, "Failed to fetch results");
    }
};
