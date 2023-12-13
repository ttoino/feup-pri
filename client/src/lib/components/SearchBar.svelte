<script lang="ts">
    import { browser } from "$app/environment";

    const query = browser
        ? new URLSearchParams(window.location.search).get("query")
        : "";
</script>

<form action="/search">
    <input
        type="search"
        class="rounded-md"
        name="query"
        id="query"
        value={query}
    />
    <button type="submit">Search</button>
</form>
