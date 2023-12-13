<script lang="ts">
    import { page } from "$app/stores";
    import errorImage from "$lib/images/error.webp";
</script>

<img src={errorImage} alt="Error" class="h-auto w-32 md:w-64" />
<h2 class="h1 text-gold-1">{$page.status}</h2>
<h3 class="h2">{$page.error?.message}</h3>
