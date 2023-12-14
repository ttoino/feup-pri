<script lang="ts">
    import Date from "$lib/components/Date.svelte";
    import Image from "$lib/components/Image.svelte";
    import Story from "$lib/components/Story.svelte";

    export let data;
</script>

<svelte:head>
    <title>{data.story.title} - LUIS</title>
    <meta name="description" content="" />
</svelte:head>

<Image
    url={data.story.image}
    alt=""
    class="-mt-8 max-h-[calc(100vh-20rem)] w-screen max-w-none object-cover md:-mt-16"
/>

<h2 class="h1 mt-16 text-center text-gold-1">{data.story.title}</h2>

{#if data.story.author}
    <p class="h3 text-center text-grey-1.5 before:content-['By_']">
        {data.story.author}
    </p>
{/if}

{#if data.story.date}
    <p class="stat-number">
        <Date date={data.story.date} format="long-date" />
    </p>
{/if}

<section class="prose prose-invert mt-16">
    {@html data.story.content}
</section>

{#if data.otherStories.length > 0}
    <h2 class="h1 mb-8 mt-16 text-center text-gold-1">More stories</h2>
    <div class="relative max-w-full">
        <div
            class="absolute bottom-0 left-0 top-0 z-10 w-16 bg-gradient-to-r from-blue-6 to-transparent"
        />
        <ol class="relative flex max-w-full flex-row gap-8 overflow-auto px-16 snap-x">
            {#each data.otherStories as story (story.id)}
                <li class="w-72 max-w-full flex-shrink-0">
                    <Story {story} />
                </li>
            {/each}
        </ol>
        <div
            class="absolute bottom-0 right-0 top-0 z-10 w-16 bg-gradient-to-l from-blue-6 to-transparent"
        />
    </div>
{/if}

{#if data.story["related_champions.name"]?.length > 0}
    <h2 class="h1 mb-8 mt-16 text-center text-gold-1">Related Champions</h2>
    {#each data.story["related_champions.name"] as champion, i}
        <!-- <Image url={champion.image}/> -->
       <a class="underline" href="{data.story["related_champions.id"][i]}-bio"> {champion} </a>
    {/each}
{/if}