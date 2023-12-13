<script lang="ts">
    import "../app.pcss";

    import Header from "$lib/components/Header.svelte";
</script>

<div class="flex min-h-full flex-col items-center">
    <Header />

    <main
        class="flex w-full max-w-screen-2xl flex-1 flex-col items-center justify-center p-8 md:p-16"
    >
        <slot />
    </main>
</div>
