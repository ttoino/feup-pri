<script lang="ts">
    export let data;
</script>

<img src={data.story.image} alt="">

<h2 class="h1 text-gold-1 mt-4">{data.story.title}</h2>

{#if data.story.author}
    <p class="h3 text-grey-1.5 before:content-['By_']">{data.story.author}</p>
{/if}

<section class="prose prose-invert mt-8">
    {@html data.story.content}
</section>
