<script lang="ts">
    import Story from "$lib/components/Story.svelte";

    export let data;
</script>

<ol
    class="grid grid-cols-[repeat(auto-fit,minmax(min(theme(spacing.72),100%),1fr))] gap-4"
>
    {#each data.results as story}
        <li>
            <Story {story} />
        </li>
    {:else}
        <p>No results found</p>
    {/each}
</ol>
