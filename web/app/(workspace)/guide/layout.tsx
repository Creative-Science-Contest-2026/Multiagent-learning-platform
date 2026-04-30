import { redirect } from "next/navigation";

export default function GuideLayout() {
  // Feature remains in-repo for later reactivation; public entry is temporarily disabled.
  redirect("/playground");
}
