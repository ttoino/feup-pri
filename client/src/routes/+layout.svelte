<script lang="ts">
    import "../app.pcss";

    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";
    import { navigating } from "$app/stores";
    import Loading from "$lib/components/Loading.svelte";
</script>

<div class="flex min-h-full flex-col items-center">
    <Header />

    <main
        class="flex w-full max-w-screen-2xl flex-1 flex-col items-center justify-center p-8 transition-opacity md:p-16"
        class:opacity-0={$navigating}
    >
        <slot />
    </main>

    <Loading />

    <Footer />
</div>
