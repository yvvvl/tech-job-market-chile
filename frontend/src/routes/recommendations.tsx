import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowRight,
  Clock,
  GraduationCap,
  Sparkles,
  TrendingUp,
  Wallet,
} from "lucide-react";
import type { ReactNode } from "react";

import { AppShell } from "@/components/layout/AppShell";
import { PageHeader, Section } from "@/components/ui-kit/Section";
import { formatCLP } from "@/lib/mockData";
import { getRecommendations, type LearningPath } from "@/lib/api/market";
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

  const recommendations = useQuery({
    queryKey: ["recommendations"],
    queryFn: getRecommendations,
  });

  if (recommendations.isLoading) {
    return (
      <AppShell>
        <PageHeader
          eyebrow={t("rec.eyebrow")}
          title={t("rec.title")}
          description="Calculando rutas de carrera desde la API..."
        />

        <div className="rounded-2xl border border-border/60 bg-card/50 p-6 shadow-card">
          <p className="text-sm text-muted-foreground">
            Cargando recomendaciones basadas en tecnologías reales del backend...
          </p>
        </div>
      </AppShell>
    );
  }

  if (recommendations.isError || !recommendations.data) {
    return (
      <AppShell>
        <PageHeader
          eyebrow={t("rec.eyebrow")}
          title={t("rec.title")}
          description="No se pudieron cargar las recomendaciones."
        />

        <div className="rounded-2xl border border-destructive/40 bg-card/50 p-6 shadow-card">
          <p className="text-sm text-destructive">
            Error conectando con la API. Revisa que FastAPI esté corriendo en localhost:8000.
          </p>
        </div>
      </AppShell>
    );
  }

  const learningPaths = recommendations.data.learningPaths;
  const suggested = recommendations.data.suggested;

  return (
    <AppShell>
      <PageHeader
        eyebrow={t("rec.eyebrow")}
        title={t("rec.title")}
        description={t("rec.desc")}
      />

      <div className="grid gap-6 md:grid-cols-2">
        {learningPaths.map((path) => (
          <CareerPathCard key={path.title} path={path} />
        ))}
      </div>

      <div className="mt-10">
        <Section
          title={t("rec.suggested.title")}
          description={t("rec.suggested.desc")}
        >
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {suggested.map((tech) => (
              <Link
                key={tech.name}
                to="/explorer"
                className="flex items-center justify-between rounded-xl border border-border/60 bg-background/40 p-4 transition hover:border-primary/40"
              >
                <div>
                  <p className="text-sm font-semibold">{tech.name}</p>
                  <p className="text-xs text-muted-foreground">{tech.category}</p>
                </div>

                <div className="text-right">
                  <p className="font-mono text-xs">{tech.demand.toLocaleString()}</p>
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

function CareerPathCard({ path }: { path: LearningPath }) {
  const t = useT();
  const keys = pathKeyMap[path.title];

  const title = keys ? t(keys.title) : path.title;
  const description = keys ? t(keys.desc) : path.description;

  return (
    <article className="group relative overflow-hidden rounded-2xl border border-border/60 bg-card/60 p-6 shadow-card transition hover:border-primary/40">
      <div className="pointer-events-none absolute inset-0 bg-hero opacity-0 transition group-hover:opacity-100" />

      <div className="relative flex items-start justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-border/60 bg-background/60 px-2.5 py-1 text-[11px] text-muted-foreground">
            <GraduationCap className="h-3 w-3 text-primary" />
            {t("rec.path")}
          </div>

          <h3 className="mt-3 font-display text-xl font-semibold tracking-tight">
            {title}
          </h3>

          <p className="mt-2 max-w-md text-sm text-muted-foreground">
            {description}
          </p>
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

      <div className="relative mt-4 rounded-xl border border-border/60 bg-background/40 px-3 py-2.5">
        <div className="flex items-center justify-between gap-3 text-xs">
          <span className="inline-flex items-center gap-1.5 text-muted-foreground">
            <Wallet className="h-3.5 w-3.5 text-primary" />
            Salario promedio estimado
          </span>

          <span className="font-mono">
            {formatCLP(path.avgSalaryCLP)}
          </span>
        </div>
      </div>

      <div className="relative mt-5">
        <p className="mb-2 text-[11px] uppercase tracking-[0.15em] text-muted-foreground">
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
          className="inline-flex items-center gap-1 text-primary transition-all hover:gap-2"
        >
          {t("rec.exploreStack")} <ArrowRight className="h-3 w-3" />
        </Link>
      </div>
    </article>
  );
}

function Indicator({
  icon,
  label,
  value,
}: {
  icon: ReactNode;
  label: string;
  value: number;
}) {
  const safeValue = Math.min(Math.max(value, 0), 100);

  return (
    <div className="rounded-xl border border-border/60 bg-background/40 px-3 py-2.5">
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground">
        <span className="text-primary">{icon}</span>
        <span>{label}</span>
      </div>

      <div className="mt-2 flex items-center gap-2">
        <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-primary"
            style={{ width: `${safeValue}%` }}
          />
        </div>

        <span className="font-mono text-xs">{value}</span>
      </div>
    </div>
  );
}