<script lang="ts">
    import logoImage from "$lib/images/logo.svg";
    import { MetaTags } from "svelte-meta-tags";
</script>

<MetaTags
    title="Home"
    description="Discover the League of Legends Universe"
    titleTemplate="%s - LUIS"
    openGraph={{
        type: "website",
        siteName: "LUIS",
        title: "Home",
        images: [
            {
                url: logoImage,
            },
        ],
    }}
/>

<enhanced:img src="$lib/images/home.webp" alt="" class="h-auto w-32 md:w-64" />
<h1 class="h3 text-gold-4">
    <span>Discover the League of Legends Universe</span>
</h1>
<h2 class="h4 mb-10 text-gold-2">
    <span>Dive into this magical world full of wonders and fantasy...</span>
</h2>

<a
    class="h3 group bg-gradient-to-br from-gold-5 via-gold-4 to-gold-1 p-[4px] transition-all duration-300 [background-size:200%_200%] hover:shadow-lg hover:[background-position:100%_100%]"
    href="/search?query="
>
    <span
        class="inline-block bg-gradient-to-bl from-blue-4 via-blue-5 to-blue-6 px-12 py-2 text-gold-1 transition-all duration-300 [background-size:200%_200%] [background-position:0%_100%] group-hover:text-gold-4 group-hover:[background-position:100%_0%]"
    >
        All stories
    </span>
</a>
