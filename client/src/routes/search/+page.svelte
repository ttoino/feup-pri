<script lang="ts">
    import Story from "$lib/components/Story.svelte";
    import Pagination from "./Pagination.svelte";
    import { fly } from "svelte/transition";
    import Profile from "$lib/components/Profile.svelte";
    import logoImage from "$lib/images/logo.svg?enhanced";
    import { MetaTags } from "svelte-meta-tags";

    export let data;
</script>

<MetaTags
    title={data.query || 'Search'}
    description="Search results for {data.query}"
    titleTemplate="%s - LUIS"
    openGraph={{
        siteName: "LUIS",
        title: data.query || 'Search',
        images: [
            {
                url: logoImage,
            },
        ],
    }}
/>

<h2 class="h1 mb-4 self-start">
    {#if data.query}
        Search results for <span class="italic">{data.query}</span>
    {:else}
        All stories
    {/if}
</h2>

{#if data.spellcheck && data.spellcheck.length > 0}
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
