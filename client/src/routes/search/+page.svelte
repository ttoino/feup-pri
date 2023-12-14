<script lang="ts">
    import Story from "$lib/components/Story.svelte";
    import { flip } from "svelte/animate";
    import Pagination from "./Pagination.svelte";
    import { fly } from "svelte/transition";
    import Profile from "$lib/components/Profile.svelte";

    export let data;
</script>

<svelte:head>
    <title>{data.query || "Search"} - LUIS</title>
    <meta name="description" content="Search results" />
</svelte:head>

<h2 class="h1 mb-4 self-start">
    {#if data.query}
        Search results for <span class="italic">{data.query}</span>
    {:else}
        All stories
    {/if}
</h2>

{#if data.spellcheck?.length ?? 0 > 0}
    <p class="mb-4 self-start">
        Did you mean
        {#each data.spellcheck as spellcheck, i}
            {i > 0 ? " or " : ""}
            <a
                class="italic text-gold-3"
                href="?query={encodeURIComponent(spellcheck)}"
            >
                {spellcheck}</a
            >{/each}?
    </p>
{/if}

<ol
    class="grid grid-cols-[repeat(auto-fill,minmax(min(theme(spacing.72),100%),1fr))] gap-4"
>
    {#if data.profile != null}
        <li class="col-span-full border-b-2 border-gold-4 pb-4">
            <Profile profile={data.profile} />
        </li>
    {/if}

    {#each data.results as story, i (story.id)}
        <li
            in:fly={{
                delay: 100 * i,
                y: 100,
            }}
        >
            <Story {story} />
        </li>
    {:else}
        <p>No results found</p>
    {/each}
</ol>

<Pagination pages={data.pages} current={data.current} />
