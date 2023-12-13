<script lang="ts">
    import SearchBar from "./SearchBar.svelte";
</script>

<header class="flex flex-row items-center justify-between self-stretch p-4">
    <h1 class="h3 text-gold-1">
        <span class="sr-only md:not-sr-only">
            LoL Universe Indexing and Search
        </span>
        <span class="md:hidden" aria-hidden="true">LUIS</span>
    </h1>

    <SearchBar />
</header>
