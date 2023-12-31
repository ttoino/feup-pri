import type { PageLoad } from "./$types";
import { redirect } from "@sveltejs/kit";

export const load: PageLoad = async ({ params: { story } }) => {
    redirect(308, `/story/${story}`);
};
