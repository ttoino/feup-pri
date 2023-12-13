<script lang="ts">
    import type { Story } from "$lib/documents";
    import Image from "./Image.svelte";

    export let story: Story;
</script>

<article
    class="group relative flex h-full flex-col gap-[2px] bg-gradient-to-br from-gold-5 via-gold-4 to-gold-1 p-[4px] transition-all duration-300 [background-size:200%_200%] hover:shadow-lg hover:[background-position:100%_100%]"
>
    <Image
        url={story.image}
        alt={story.title}
        class="aspect-video h-auto w-full object-cover"
    />

    <div
        class="flex-1 bg-gradient-to-bl from-blue-4 via-blue-5 to-blue-6 p-4 transition-all duration-300 [background-size:200%_200%] [background-position:0%_100%] group-hover:[background-position:100%_0%]"
    >
        <a href="/story/{story.id}" class="after:absolute after:inset-0">
            <h3
                class="h4 truncate text-gold-3 transition-colors duration-300 group-hover:text-gold-1"
            >
                {story.title}
            </h3>
        </a>

        {#if story.author}
            <p
                class="bold-label truncate transition-colors duration-300 before:content-['By_'] group-hover:text-gold-3"
            >
                {story.author}
            </p>
        {/if}

        <section
            class="prose truncate whitespace-normal text-grey-1.5 transition-colors duration-300 group-hover:text-grey-1 prose-p:m-0 prose-hr:hidden"
            class:line-clamp-4={!story.author}
            class:line-clamp-3={story.author}
        >
            {@html story.content}
        </section>
    </div>
</article>
