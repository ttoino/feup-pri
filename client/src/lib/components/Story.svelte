<script lang="ts">
    import type { Story } from "$lib/documents";

    export let story: Story;
</script>

<article
    class="relative h-full bg-gradient-to-tl from-gold-4 to-gold-5 p-[4px] transition-all hover:bg-gradient-to-tr hover:from-gold-5 hover:to-gold-4 flex flex-col gap-[2px]"
>
        <img
            src={story.image}
            alt={story.title}
            class="aspect-video h-auto w-full object-cover"
        />

        <div class="p-4 bg-gradient-to-bl from-blue-5 to-blue-6 flex-1">
            <a href="/story/{story.id}" class="after:absolute after:inset-0">
                <h3 class="h4 truncate text-gold-1">{story.title}</h3>
            </a>

            {#if story.author}
                <p class="bold-label truncate before:content-['By_']">
                    {story.author}
                </p>
            {/if}

            <section
                class="prose line-clamp-3 truncate whitespace-normal text-grey-1.5 prose-p:m-0"
            >
                {@html story.content}
            </section>
        </div>
</article>
