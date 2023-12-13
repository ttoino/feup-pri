import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config}*/
const config = {
    content: ["./src/**/*.{html,js,svelte,ts}"],

    theme: {
        colors: {
            inherit: "inherit",
            transparent: "transparent",
            current: "currentColor",
            blue: {
                1: "#cdfafa",
                2: "#0ac8b9",
                3: "#0397ab",
                4: "#005a82",
                5: "#0a323c",
                6: "#091428",
                7: "#0a1428",
            },
            gold: {
                1: "#F0E6D2",
                2: "#C8AA6E",
                3: "#C8AA6E",
                4: "#C89B3C",
                5: "#785A28",
                6: "#463714",
                7: "#32281E",
            },
            grey: {
                1: "#A09B8C",
                1.5: "#5B5A56",
                2: "#3C3C41",
                3: "#1E2328",
                cool: "#1E282D",
            },
            hextechBlack: "#010A13",
        },
        // typography: (theme) => ({
        //     DEFAULT: {
        //         css: {
        //             "--tw-prose-body": theme("colors.grey[1.5]"),
        //             "--tw-prose-headings": theme("colors.grey[1]"),
        //             "--tw-prose-lead": theme("colors.pink[700]"),
        //             "--tw-prose-links": theme("colors.pink[900]"),
        //             "--tw-prose-bold": theme("colors.pink[900]"),
        //             "--tw-prose-counters": theme("colors.pink[600]"),
        //             "--tw-prose-bullets": theme("colors.pink[400]"),
        //             "--tw-prose-hr": theme("colors.pink[300]"),
        //             "--tw-prose-quotes": theme("colors.pink[900]"),
        //             "--tw-prose-quote-borders": theme("colors.pink[300]"),
        //             "--tw-prose-captions": theme("colors.pink[700]"),
        //             "--tw-prose-code": theme("colors.pink[900]"),
        //             "--tw-prose-pre-code": theme("colors.pink[100]"),
        //             "--tw-prose-pre-bg": theme("colors.pink[900]"),
        //             "--tw-prose-th-borders": theme("colors.pink[300]"),
        //             "--tw-prose-td-borders": theme("colors.pink[200]"),
        //         },
        //     },
        // }),
        fontFamily: {
            sans: ["Spiegel", "sans-serif"],
            serif: ["Beaufort for LOL", "serif"],
            mono: ["monospace"],
        },

        extend: {},
    },

    plugins: [typography],
};

module.exports = config;
