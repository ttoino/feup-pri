<script lang="ts">
    import Image from "$lib/components/Image.svelte";
    import liliaImage from "$lib/images/home.webp";
    import SearchBar from "$lib/components/SearchBar.svelte";
</script>

<svelte:head>
    <title>LUIS</title>
    <meta name="description" content="Svelte demo app" />
</svelte:head>

<Image url={liliaImage} />
<h1 class="h3 text-gold-4">
    <span> Discover League of Legends Universe </span>
</h1>
<h2 class="h4 mb-10 text-gold-2">
    <span> Dive into this magical world full of wonders and fantasy...</span>
</h2>

<SearchBar />
