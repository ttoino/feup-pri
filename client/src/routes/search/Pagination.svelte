<script lang="ts">
    import { page } from "$app/stores";
    import { ChevronLeft, ChevronRight, Icon } from "svelte-hero-icons";

    export let pages: number;
    export let current: number;

    const hrefToPage = (to: number) => {
        const params = new URLSearchParams($page.url.searchParams);
        params.set("page", to.toString());
        return `?${params.toString()}`;
    };
</script>

{#if pages > 1}
    <div class="mt-8 max-w-full snap-x snap-mandatory overflow-auto">
        <nav
            class="stat-number grid w-max grid-flow-col items-stretch justify-center leading-[1] [grid-auto-columns:1fr]"
        >
            {#if current > 1}
                <a
                    href={hrefToPage(current - 1)}
                    class="inline-flex snap-center items-center justify-center border-2 border-l-0 border-gold-4 p-2 text-gold-1 first:border-l-2"
                >
                    <Icon src={ChevronLeft} class="h-[1em] w-[1em]" />
                </a>
            {/if}

            {#each Array(pages).keys() as page}
                <a
                    href={hrefToPage(page + 1)}
                    class="inline-flex snap-center items-center justify-center border-2 border-l-0 border-gold-4 p-2 text-gold-1 first:border-l-2"
                    class:text-gold-1={page + 1 === current}
                >
                    {page + 1}
                </a>
            {/each}

            {#if current < pages}
                <a
                    href={hrefToPage(current + 1)}
                    class="inline-flex snap-center items-center justify-center border-2 border-l-0 border-gold-4 p-2 text-gold-1 first:border-l-2"
                >
                    <Icon src={ChevronRight} class="h-[1em] w-[1em]" />
                </a>
            {/if}
        </nav>
    </div>
{/if}
