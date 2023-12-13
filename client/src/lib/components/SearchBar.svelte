<script lang="ts">
    import { browser } from "$app/environment";
    import { onNavigate } from "$app/navigation";
    import { Icon, MagnifyingGlass, XMark } from "svelte-hero-icons";

    let query = browser
        ? new URLSearchParams(window.location.search).get("query")
        : "";

    let open = false;

    onNavigate((event) => {
        const routeQuery = new URLSearchParams(event.to?.url.search).get(
            "query",
        );
        if (routeQuery) query = routeQuery;
    });
</script>

<button
    aria-hidden="true"
    class="p-2 sm:hidden"
    on:click={() => (open = !open)}
>
    <Icon src={open ? XMark : MagnifyingGlass} class="h-6 w-6" />
</button>

<form
    action="/search"
    class="grid w-full overflow-hidden transition-[grid-template-rows] sm:w-96 sm:grid-rows-1 {open
        ? 'grid-rows-[1fr]'
        : 'grid-rows-[0fr]'}"
    data-sveltekit-keepfocus
>
    <div class="min-h-0">
        <div
            class="relative mt-4 bg-gradient-to-tl from-gold-4 to-gold-5 p-[2px] sm:m-0"
        >
            <label for="query" class="sr-only">Query</label>
            <input
                type="search"
                class="min-h-0 w-full bg-gradient-to-bl from-blue-5 to-blue-6 p-2 pr-12 !outline-none placeholder:text-grey-1.5"
                name="query"
                id="query"
                placeholder="Search"
                value={query}
            />
            <button
                type="submit"
                class="absolute bottom-0 right-0 top-0 flex aspect-square h-full items-center justify-center text-gold-4"
            >
                <span class="sr-only"> Search </span>
                <Icon src={MagnifyingGlass} class="h-6 w-6" />
            </button>
        </div>
    </div>
</form>
