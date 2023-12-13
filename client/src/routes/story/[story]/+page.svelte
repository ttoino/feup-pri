<script lang="ts">
    import Date from "$lib/components/Date.svelte";
    import Image from "$lib/components/Image.svelte";

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


{#each data.otherStories.slice(0, 5) as item (item.id)}
   <a href={item.id}>
    <Image 
            url={item.image}
            alt=""
        />
        <h3 class="h3">{item.title}</h3>
    </a>
{/each}


<section class="prose prose-invert mt-16">
    {@html data.story.content}
</section>
