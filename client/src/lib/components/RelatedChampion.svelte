<script lang="ts">
    import Image from "./Image.svelte";

    export let name: string;
    export let image: string;
    export let title: string;
</script>

<a
    href="/search?query={encodeURIComponent(name)}"
    class="flex w-40 flex-col items-center"
>
    <Image
        url={image}
        alt={name}
        class="h-36 w-36 rounded-full border-4 border-gold-3 object-cover"
    />

    <h3 class="h3 text-gold-1.5 text-center">{name}</h3>
    <p class="bold-label text-center text-grey-1.5">{title}</p>
</a>
