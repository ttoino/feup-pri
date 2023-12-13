<script lang="ts">
    const formats = {
        short: {
            month: "short",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
        },
        long: {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
        },

        "short-date": {
            month: "short",
            day: "numeric",
        },
        "long-date": {
            year: "numeric",
            month: "long",
            day: "numeric",
        },
    } as const satisfies Record<string, Parameters<Date["toLocaleString"]>[1]>;

    export let date: ConstructorParameters<typeof Date>[0];
    export let format: keyof typeof formats = "short";

    $: dateObj = new Date(date);
    $: formattedDate = dateObj.toLocaleDateString(undefined, formats[format]);
</script>

<time datetime={dateObj.toISOString()}>{formattedDate}</time>
