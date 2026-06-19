import { Link } from "@tanstack/react-router";
import {
  BarChart3,
  Compass,
  GraduationCap,
  LayoutDashboard,
  Languages,
  LineChart,
} from "lucide-react";
import type { ReactNode } from "react";
import { useI18n } from "@/lib/i18n-hooks";

export function AppShell({ children }: { children: ReactNode }) {
  const { lang, setLang, t } = useI18n();

  type NavItem = {
    to: "/" | "/dashboard" | "/explorer" | "/recommendations";
    label: string;
    icon: typeof LineChart;
    exact?: boolean;
  };

  const navItems: NavItem[] = [
    { to: "/", label: t("nav.overview"), icon: LineChart, exact: true },
    { to: "/dashboard", label: t("nav.dashboard"), icon: LayoutDashboard },
    { to: "/explorer", label: t("nav.explorer"), icon: Compass },
    {
      to: "/recommendations",
      label: t("nav.recommendations"),
      icon: GraduationCap,
    },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-40 border-b border-border/60 bg-background/70 backdrop-blur-xl">
        <div className="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-6">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="grid h-8 w-8 place-items-center rounded-lg bg-primary/15 text-primary ring-1 ring-primary/30 group-hover:bg-primary/25 transition">
              <BarChart3 className="h-4 w-4" />
            </div>
            <div className="flex flex-col leading-tight">
              <span className="text-sm font-semibold tracking-tight">
                TechMarket CL
              </span>
              <span className="text-[10px] uppercase tracking-[0.15em] text-muted-foreground">
                {t("brand.tagline")}
              </span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-1 rounded-full border border-border/60 bg-card/50 p-1">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                activeOptions={{ exact: item.exact }}
                className="px-4 py-1.5 text-sm text-muted-foreground rounded-full hover:text-foreground transition data-[status=active]:bg-primary/15 data-[status=active]:text-foreground"
              >
                {item.label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setLang(lang === "en" ? "es" : "en")}
              aria-label={t("lang.aria")}
              className="inline-flex items-center gap-1.5 rounded-full border border-border/60 bg-card/50 px-3 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground hover:border-primary/40 transition"
            >
              <Languages className="h-3.5 w-3.5" />
              {t("lang.toggle")}
            </button>
            <Link
              to="/dashboard"
              className="hidden sm:inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:opacity-90 transition shadow-glow"
            >
              {t("cta.exploreInsights")}
            </Link>
          </div>
        </div>
        <nav className="md:hidden flex items-center justify-around border-t border-border/60 bg-background/80 py-2">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              activeOptions={{ exact: item.exact }}
              className="flex flex-col items-center text-[10px] text-muted-foreground gap-0.5 data-[status=active]:text-primary"
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          ))}
        </nav>
      </header>
      <main className="mx-auto w-full max-w-7xl px-6 py-10">{children}</main>
      <footer className="border-t border-border/60 mt-16">
        <div className="mx-auto max-w-7xl px-6 py-8 text-xs text-muted-foreground flex flex-col sm:flex-row gap-2 justify-between">
          <span>
            © {new Date().getFullYear()} TechMarket CL — {t("footer.copy")}
          </span>
          <span>{t("footer.note")}</span>
        </div>
      </footer>
    </div>
  );
}
