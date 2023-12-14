<script lang="ts">
    import SearchBar from "./SearchBar.svelte";
    import { Icon, Home } from "svelte-hero-icons";
</script>

<header
    class="sticky top-0 z-10 flex flex-row flex-wrap items-center justify-between gap-x-4 self-stretch bg-gradient-to-b from-blue-6 to-blue-7 p-4 shadow-xl sm:flex-nowrap"
>
    <a href="/" class="p-2 text-gold-3"><Icon src={Home} class="h-8 w-8" /></a>

    <h1 class="h3 mr-auto text-gold-3">
        <span class="sr-only lg:not-sr-only">
            LoL Universe Indexing and Search
        </span>
        <span class="lg:hidden" aria-hidden="true">LUIS</span>
    </h1>

    <SearchBar />
</header>
