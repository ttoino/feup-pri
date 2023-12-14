<script lang="ts">
    import Image from "$lib/components/Image.svelte";
    import liliaImage from "$lib/images/home.webp";
    import SearchBar from "$lib/components/SearchBar.svelte";
</script>

<svelte:head>
    <title>LUIS</title>
    <meta name="description" content="Svelte demo app" />
</svelte:head>

<Image url={liliaImage}/>
<h1 class="h3 text-gold-4">
    <span class="sr-only md:not-sr-only"> Discover League of Legends Universe </span>
    <span class="md:hidden" aria-hidden="true">LUIS</span>
</h1>
<h2 class="h4 text-gold-2">
    <span class="sr-only md:not-sr-only"> Dive into this magical world full of wonders and fantasy...</span>
    <span class="md:hidden" aria-hidden="true">LUIS</span>
</h2>
