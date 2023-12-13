<script lang="ts">
    import { browser } from "$app/environment";
    import { onMount } from "svelte";
    import type { HTMLImgAttributes } from "svelte/elements";

    interface $Props extends Omit<HTMLImgAttributes, "src"> {
        url: string;
    }

    export let url: string;

    let loaded = false;
    $: src = loaded ? url : `${url}?width=100`;

    onMount(() => {
        if (browser) {
            const img = new Image();
            img.onload = () => {
                loaded = true;
            };
            img.src = url;
        }
    });
</script>

<img
    {src}
    {...$$restProps}
    class:blur-lg={!loaded}
    class="overflow-hidden blur-0 transition {$$restProps.class}"
/>
