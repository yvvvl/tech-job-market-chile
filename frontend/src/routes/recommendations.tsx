import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, Clock, GraduationCap, Sparkles, TrendingUp } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader, Section } from "@/components/ui-kit/Section";
import { learningPaths, technologies } from "@/lib/mockData";
import { useT } from "@/lib/i18n";

export const Route = createFileRoute("/recommendations")({
  head: () => ({
    meta: [
      { title: "Career Recommendations — TechMarket CL" },
      {
        name: "description",
        content:
          "Personalized learning paths and technology suggestions based on real Chilean market demand.",
      },
    ],
  }),
  component: RecommendationsPage,
});

const pathKeyMap: Record<string, { title: string; desc: string }> = {
  "Frontend Engineer": { title: "path.frontend.title", desc: "path.frontend.desc" },
  "Backend Engineer": { title: "path.backend.title", desc: "path.backend.desc" },
  "Data Analyst": { title: "path.data.title", desc: "path.data.desc" },
  "Cloud & DevOps": { title: "path.cloud.title", desc: "path.cloud.desc" },
};

function RecommendationsPage() {
  const t = useT();
  const suggested = [...technologies]
    .sort((a, b) => b.juniorFriendly * b.demand - a.juniorFriendly * a.demand)
    .slice(0, 6);

  return (
    <AppShell>
      <PageHeader
        eyebrow={t("rec.eyebrow")}
        title={t("rec.title")}
        description={t("rec.desc")}
      />

      <div className="grid md:grid-cols-2 gap-6">
        {learningPaths.map((path) => {
          const keys = pathKeyMap[path.title];
          const title = keys ? t(keys.title) : path.title;
          const description = keys ? t(keys.desc) : path.description;
          return (
            <article
              key={path.title}
              className="group relative overflow-hidden rounded-2xl border border-border/60 bg-card/60 p-6 shadow-card hover:border-primary/40 transition"
            >
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition bg-hero pointer-events-none" />
              <div className="relative flex items-start justify-between">
                <div>
                  <div className="inline-flex items-center gap-2 rounded-full border border-border/60 bg-background/60 px-2.5 py-1 text-[11px] text-muted-foreground">
                    <GraduationCap className="h-3 w-3 text-primary" />
                    {t("rec.path")}
                  </div>
                  <h3 className="mt-3 font-display text-xl font-semibold tracking-tight">
                    {title}
                  </h3>
                  <p className="mt-2 text-sm text-muted-foreground max-w-md">{description}</p>
                </div>
                <div className="text-right">
                  <p className="text-[10px] uppercase tracking-[0.15em] text-muted-foreground">
                    {t("rec.demandScore")}
                  </p>
                  <p className="font-display text-2xl font-semibold text-gradient">
                    {path.demandScore}
                  </p>
                </div>
              </div>

              <div className="relative mt-5 grid grid-cols-2 gap-3">
                <Indicator
                  icon={<TrendingUp className="h-3.5 w-3.5" />}
                  label={t("rec.indicator.demand")}
                  value={path.demandScore}
                />
                <Indicator
                  icon={<Sparkles className="h-3.5 w-3.5" />}
                  label={t("rec.indicator.junior")}
                  value={path.juniorScore}
                />
              </div>

              <div className="relative mt-5">
                <p className="text-[11px] uppercase tracking-[0.15em] text-muted-foreground mb-2">
                  {t("rec.stack")}
                </p>
                <div className="flex flex-wrap gap-2">
                  {path.techs.map((tech) => (
                    <span
                      key={tech}
                      className="inline-flex items-center rounded-full border border-border/70 bg-background/60 px-2.5 py-1 text-xs"
                    >
                      {tech}
                    </span>
                  ))}
                </div>
              </div>

              <div className="relative mt-6 flex items-center justify-between text-xs text-muted-foreground">
                <span className="inline-flex items-center gap-1">
                  <Clock className="h-3.5 w-3.5" /> ~{path.timeWeeks} {t("rec.weeks")}
                </span>
                <Link
                  to="/explorer"
                  className="inline-flex items-center gap-1 text-primary hover:gap-2 transition-all"
                >
                  {t("rec.exploreStack")} <ArrowRight className="h-3 w-3" />
                </Link>
              </div>
            </article>
          );
        })}
      </div>

      <div className="mt-10">
        <Section
          title={t("rec.suggested.title")}
          description={t("rec.suggested.desc")}
        >
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {suggested.map((tech) => (
              <Link
                key={tech.name}
                to="/explorer"
                className="rounded-xl border border-border/60 bg-background/40 p-4 hover:border-primary/40 transition flex items-center justify-between"
              >
                <div>
                  <p className="text-sm font-semibold">{tech.name}</p>
                  <p className="text-xs text-muted-foreground">{tech.category}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs font-mono">{tech.demand.toLocaleString()}</p>
                  <p className="text-[10px] text-[color:var(--color-success)]">
                    {tech.juniorFriendly}% {t("rec.juniorSuffix")}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </Section>
      </div>
    </AppShell>
  );
}

function Indicator({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: number;
}) {
  return (
    <div className="rounded-xl border border-border/60 bg-background/40 px-3 py-2.5">
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground">
        <span className="text-primary">{icon}</span>
        {label}
      </div>
      <div className="mt-2 flex items-center gap-2">
        <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full"
            style={{ width: `${value}%`, background: "var(--gradient-primary)" }}
          />
        </div>
        <span className="font-mono text-xs">{value}</span>
      </div>
    </div>
  );
}
