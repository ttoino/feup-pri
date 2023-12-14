<script lang="ts">
    import Story from "$lib/components/Story.svelte";
    import { flip } from "svelte/animate";
    import Pagination from "./Pagination.svelte";
    import { fly } from "svelte/transition";

    export let data;
</script>

<svelte:head>
    <title>{data.query || "Search"} - LUIS</title>
    <meta name="description" content="Search results" />
</svelte:head>

<ol
    class="grid grid-cols-[repeat(auto-fill,minmax(min(theme(spacing.72),100%),1fr))] gap-4"
>
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
