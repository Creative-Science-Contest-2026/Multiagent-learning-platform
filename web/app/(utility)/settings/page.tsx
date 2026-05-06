"use client";

import { useEffect, useState } from "react";

import { useTranslation } from "react-i18next";

import { writeStoredLanguage, type AppLanguage } from "@/context/AppShellContext";
import { apiFetch } from "@/lib/api";
import { setTheme as applyThemePreference } from "@/lib/theme";

type UiSettings = {
  theme: "light" | "dark";
  language: AppLanguage;
};

type SettingsPayload = {
  ui: UiSettings;
};

function SettingsPageContent() {
  const { t } = useTranslation();
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const [language, setLanguage] = useState<AppLanguage>("en");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const load = async () => {
      const response = await apiFetch("/api/v1/settings");
      const payload = (await response.json()) as SettingsPayload;
      setTheme(payload.ui.theme);
      setLanguage(payload.ui.language);
    };

    void load();
  }, []);

  useEffect(() => {
    if (!message) return;
    const timer = window.setTimeout(() => setMessage(""), 2500);
    return () => window.clearTimeout(timer);
  }, [message]);

  const persistUi = async (nextTheme: "light" | "dark", nextLanguage: AppLanguage) => {
    await apiFetch("/api/v1/settings/ui", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ theme: nextTheme, language: nextLanguage }),
    });
  };

  const updateTheme = async (nextTheme: "light" | "dark") => {
    setTheme(nextTheme);
    applyThemePreference(nextTheme);
    await persistUi(nextTheme, language);
    setMessage(t("Preferences updated"));
  };

  const updateLanguage = async (nextLanguage: AppLanguage) => {
    setLanguage(nextLanguage);
    writeStoredLanguage(nextLanguage);
    await persistUi(theme, nextLanguage);
    setMessage(t("Preferences updated"));
  };

  return (
    <div className="h-full overflow-y-auto [scrollbar-gutter:stable]">
      <div className="mx-auto max-w-[960px] px-6 py-8">
        <div className="mb-8">
          <h1 className="text-[24px] font-semibold tracking-tight text-[var(--foreground)]">
            {t("Settings")}
          </h1>
          <p className="mt-1 text-[13px] text-[var(--muted-foreground)]">
            {message || t("Personal preferences are available here.")}
          </p>
        </div>

        <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-6 shadow-sm">
          <div className="grid gap-6 sm:grid-cols-2">
            <div>
              <div className="mb-2 text-[12px] text-[var(--muted-foreground)]">
                {t("Theme")}
              </div>
              <div className="flex gap-0.5 rounded-lg bg-[var(--muted)] p-0.5">
                {(["light", "dark"] as const).map((value) => (
                  <button
                    key={value}
                    onClick={() => void updateTheme(value)}
                    className={`rounded-md px-3 py-2 text-[13px] transition-all ${
                      theme === value
                        ? "bg-[var(--card)] font-medium text-[var(--foreground)] shadow-sm"
                        : "text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
                    }`}
                  >
                    {value === "light" ? t("Light") : t("Dark")}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <div className="mb-2 text-[12px] text-[var(--muted-foreground)]">
                {t("Language")}
              </div>
              <div className="flex flex-wrap gap-0.5 rounded-lg bg-[var(--muted)] p-0.5">
                {(["en", "zh", "vi"] as const).map((value) => (
                  <button
                    key={value}
                    onClick={() => void updateLanguage(value)}
                    className={`rounded-md px-3 py-2 text-[13px] transition-all ${
                      language === value
                        ? "bg-[var(--card)] font-medium text-[var(--foreground)] shadow-sm"
                        : "text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
                    }`}
                  >
                    {value === "en" ? "English" : value === "zh" ? "中文" : "Tiếng Việt"}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-6 rounded-xl border border-[var(--border)]/70 bg-[var(--muted)]/30 px-4 py-3 text-[13px] leading-6 text-[var(--muted-foreground)]">
            {t("Runtime setup is managed by administrators and loaded securely on the server.")}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function SettingsPage() {
  return <SettingsPageContent />;
}
