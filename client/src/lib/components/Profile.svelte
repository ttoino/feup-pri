<script lang="ts">
    import type { Champion } from "$lib/documents";
    import Image from "./Image.svelte";

    export let profile: Champion & { content: string };
</script>

<article
    class="group relative flex h-full flex-row gap-[2px] bg-gradient-to-br from-gold-5 via-gold-4 to-gold-1 p-[4px] transition-all duration-300 [background-size:200%_200%] hover:shadow-lg hover:[background-position:100%_100%]"
>
    <Image
        url={profile.image}
        alt="{profile.name} icon"
        class="h-full w-96 object-cover"
    />

    <div
        class="flex-1 bg-gradient-to-bl from-blue-4 via-blue-5 to-blue-6 p-4 transition-all duration-300 [background-size:200%_200%] [background-position:0%_100%] group-hover:[background-position:100%_0%]"
    >
        <a href="/story/{profile.id}-bio" class="after:absolute after:inset-0">
            <h3
                class="h4 truncate text-gold-3 transition-colors duration-300 group-hover:text-gold-1"
            >
                {profile.name}, {profile.title}
            </h3>
        </a>

        {#if profile.aliases?.length > 0}
            <ul class="inline-flex flex-row">
                {#each profile.aliases as alias}
                    <li
                        class="bold-label transition-colors duration-300 before:text-grey-1.5 before:transition-colors before:duration-300 before:content-[',_'] first:before:content-['aka_'] group-hover:text-gold-3 group-hover:before:text-grey-1"
                    >
                        {alias.replace(/\(.*\)/, "")}
                    </li>
                {/each}
            </ul>
        {/if}

        <blockquote
            class="bold-label italic transition-colors duration-300 group-hover:text-gold-3"
        >
            {profile.quote}
        </blockquote>

        {#if profile.races?.length > 0}
            <ul class="inline-flex flex-row">
                {#each profile.races as race}
                    <li
                        class="bold-label transition-colors duration-300 before:text-grey-1.5 before:transition-colors before:duration-300 before:content-[',_'] first:before:content-['is_'] group-hover:text-gold-3 group-hover:before:text-grey-1"
                    >
                        {race}
                    </li>
                {/each}
            </ul>
        {/if}

        {#if profile.origin}
            <p class="bold-label transition-colors duration-300 before:text-grey-1.5 before:transition-colors before:duration-300 before:content-['from_'] group-hover:text-gold-3 group-hover:before:text-grey-1">{profile.origin.name}</p>
        {/if}

        <section
            class="prose line-clamp-3 truncate whitespace-normal text-grey-1.5 transition-colors duration-300 group-hover:text-grey-1 prose-p:m-0 prose-hr:hidden"
        >
            {@html profile.content}
        </section>
    </div>
</article>
