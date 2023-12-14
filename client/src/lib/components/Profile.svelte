<script lang="ts">
    import type { Story } from "$lib/documents";
    import Image from "./Image.svelte";

    export let profile;
</script>

<article
    class="m-12 max-w-[30rem] from-gold-5 via-gold-4 to-gold-1 group relative flex h-full flex-col gap-[2px] bg-gradient-to-br p-[4px] transition-all duration-300 [background-size:200%_200%] hover:shadow-lg hover:[background-position:100%_100%]"
>
    <Image
        url={profile.image}
        alt="{profile.name} icon"
        class="aspect-video h-auto w-full object-cover"
    />

    <div
        class="from-blue-4 via-blue-5 to-blue-6 flex-1 bg-gradient-to-bl p-4 transition-all duration-300 [background-size:200%_200%] [background-position:0%_100%] group-hover:[background-position:100%_0%]"
    >
        <a href="/story/{profile.id}-bio" class="after:absolute after:inset-0">
            <h3
                class="h4 text-gold-3 group-hover:text-gold-1 truncate transition-colors duration-300"
            >
                {profile.name}, {profile.title}
            </h3>
        </a>

        <p> Champion </p>

        <p
            class="prose text-grey-1.5 group-hover:text-grey-1 prose-p:m-0 prose-hr:hidden line-clamp-3 truncate whitespace-normal transition-colors duration-300"
        >
            {@html profile.content}
        </p>
    </div>
</article>
