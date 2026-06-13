import { createFileRoute, Link } from "@tanstack/react-router";
import {
  ArrowRight,
  BarChart3,
  Briefcase,
  Building2,
  Cpu,
  GraduationCap,
  LineChart as LineChartIcon,
  MapPin,
  Sparkles,
  TrendingUp,
  Wallet,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { AppShell } from "@/components/layout/AppShell";
import { DarkTooltip } from "@/components/charts/ChartTooltip";
import {
  monthlyTrend,
  stats,
  technologies,
  formatNumber,
} from "@/lib/mockData";
import { useT } from "@/lib/i18n";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "TechMarket CL — Chilean Tech Job Intelligence" },
      {
        name: "description",
        content:
          "Discover what technologies companies in Chile are hiring for. Live market overview, salary insights and junior opportunities.",
      },
      { property: "og:title", content: "TechMarket CL — Chilean Tech Job Intelligence" },
      {
        property: "og:description",
        content:
          "Modern analytics dashboard for the Chilean tech job market — built for students, juniors and career switchers.",
      },
    ],
  }),
  component: LandingPage,
});

const topTechs = [...technologies].sort((a, b) => b.demand - a.demand).slice(0, 6);

function LandingPage() {
  const t = useT();
  return (
    <AppShell>
      {/* Hero */}
      <section className="relative -mt-10 overflow-hidden rounded-3xl border border-border/60 bg-card/30 px-6 py-16 sm:py-24 shadow-card">
        <div className="absolute inset-0 bg-hero" />
        <div className="absolute inset-0 bg-grid opacity-40 [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]" />
        <div className="relative mx-auto max-w-3xl text-center animate-fade-up">
          <div className="mx-auto inline-flex items-center gap-2 rounded-full border border-border/60 bg-background/60 px-3 py-1 text-xs text-muted-foreground backdrop-blur">
            <Sparkles className="h-3 w-3 text-primary" />
            {t("landing.badge")} · {formatNumber(stats.totalJobs)} {t("landing.activePostings")}
          </div>
          <h1 className="mt-6 font-display text-4xl sm:text-6xl font-semibold tracking-tight">
            <span className="text-gradient">{t("landing.h1.a")}</span>
            <br />
            <span className="text-foreground">{t("landing.h1.b")}</span>
          </h1>
          <p className="mx-auto mt-5 max-w-xl text-base text-muted-foreground">
            {t("landing.subtitle")}
          </p>
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-2 rounded-full bg-primary px-6 py-3 text-sm font-medium text-primary-foreground hover:opacity-90 transition shadow-glow"
            >
              {t("landing.cta.primary")} <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              to="/recommendations"
              className="inline-flex items-center gap-2 rounded-full border border-border bg-background/40 px-6 py-3 text-sm font-medium text-foreground hover:bg-background/80 transition"
            >
              {t("landing.cta.secondary")}
            </Link>
          </div>
        </div>

        {/* Floating chart preview */}
        <div className="relative mx-auto mt-14 max-w-4xl">
          <div className="rounded-2xl border border-border/60 bg-card/80 p-4 backdrop-blur shadow-glow">
            <div className="flex items-center justify-between px-2 pb-2">
              <div>
                <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
                  {t("landing.chart.eyebrow")}
                </p>
                <p className="font-display text-2xl font-semibold">{formatNumber(stats.totalJobs)}</p>
              </div>
              <div className="text-xs text-[color:var(--color-success)]">{t("landing.chart.delta")}</div>
            </div>
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={monthlyTrend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="heroJobs" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="var(--color-primary)" stopOpacity={0.6} />
                      <stop offset="100%" stopColor="var(--color-primary)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="var(--color-border)" vertical={false} />
                  <XAxis dataKey="month" stroke="var(--color-muted-foreground)" fontSize={11} tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--color-muted-foreground)" fontSize={11} tickLine={false} axisLine={false} />
                  <Tooltip content={<DarkTooltip />} />
                  <Area
                    type="monotone"
                    dataKey="jobs"
                    name={t("chart.jobs")}
                    stroke="var(--color-primary)"
                    fill="url(#heroJobs)"
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </section>

      {/* Market overview */}
      <section className="mt-16">
        <SectionHeading
          eyebrow={t("landing.overview.eyebrow")}
          title={t("landing.overview.title")}
          description={t("landing.overview.desc")}
        />
        <div className="mt-8 grid grid-cols-2 lg:grid-cols-4 gap-4">
          <MiniStat icon={Briefcase} label={t("stat.totalJobs")} value={formatNumber(stats.totalJobs)} hint={t("stat.hint.active")} />
          <MiniStat icon={Building2} label={t("stat.companies")} value={formatNumber(stats.companies)} hint={t("stat.hint.hiring")} />
          <MiniStat icon={Cpu} label={t("stat.technologies")} value={formatNumber(stats.technologies)} hint={t("stat.hint.tracked")} />
          <MiniStat icon={MapPin} label={t("stat.cities")} value={formatNumber(stats.cities)} hint={t("stat.hint.acrossChile")} />
        </div>
      </section>

      {/* Most demanded */}
      <section className="mt-16 grid lg:grid-cols-5 gap-6">
        <div className="lg:col-span-3 rounded-2xl border border-border/60 bg-card/50 p-6 shadow-card">
          <SectionHeading
            small
            eyebrow={t("landing.demand.eyebrow")}
            title={t("landing.demand.title")}
            description={t("landing.demand.desc")}
          />
          <div className="mt-6 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topTechs} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid stroke="var(--color-border)" horizontal={false} />
                <XAxis type="number" stroke="var(--color-muted-foreground)" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis type="category" dataKey="name" stroke="var(--color-muted-foreground)" fontSize={12} tickLine={false} axisLine={false} width={90} />
                <Tooltip content={<DarkTooltip />} cursor={{ fill: "var(--color-muted)", opacity: 0.3 }} />
                <Bar dataKey="demand" name={t("chart.postings")} fill="var(--color-primary)" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-2 grid gap-6">
          <FeatureCard
            icon={GraduationCap}
            title={t("feat.junior.title")}
            description={t("feat.junior.desc")}
            to="/dashboard"
            cta={t("feat.junior.cta")}
          />
          <FeatureCard
            icon={Wallet}
            title={t("feat.salary.title")}
            description={t("feat.salary.desc")}
            to="/dashboard"
            cta={t("feat.salary.cta")}
          />
          <FeatureCard
            icon={TrendingUp}
            title={t("feat.learn.title")}
            description={t("feat.learn.desc")}
            to="/recommendations"
            cta={t("feat.learn.cta")}
          />
        </div>
      </section>

      {/* CTA */}
      <section className="mt-20 overflow-hidden rounded-3xl border border-border/60 bg-card/50 p-10 sm:p-14 text-center relative">
        <div className="absolute inset-0 bg-hero opacity-80" />
        <div className="relative max-w-2xl mx-auto">
          <BarChart3 className="mx-auto h-8 w-8 text-primary" />
          <h2 className="mt-4 font-display text-3xl sm:text-4xl font-semibold tracking-tight text-gradient">
            {t("cta.section.title")}
          </h2>
          <p className="mt-3 text-muted-foreground">
            {t("cta.section.desc")}
          </p>
          <Link
            to="/dashboard"
            className="mt-6 inline-flex items-center gap-2 rounded-full bg-primary px-6 py-3 text-sm font-medium text-primary-foreground hover:opacity-90 transition shadow-glow"
          >
            {t("cta.section.btn")} <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>
    </AppShell>
  );
}

function SectionHeading({
  eyebrow,
  title,
  description,
  small,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  small?: boolean;
}) {
  return (
    <div className="max-w-2xl">
      {eyebrow ? (
        <p className="text-xs uppercase tracking-[0.18em] text-primary mb-2">{eyebrow}</p>
      ) : null}
      <h2 className={small ? "text-lg font-semibold tracking-tight" : "font-display text-2xl sm:text-3xl font-semibold tracking-tight"}>
        {title}
      </h2>
      {description ? <p className="mt-2 text-sm text-muted-foreground">{description}</p> : null}
    </div>
  );
}

function MiniStat({
  icon: Icon,
  label,
  value,
  hint,
}: {
  icon: typeof LineChartIcon;
  label: string;
  value: string;
  hint: string;
}) {
  return (
    <div className="rounded-2xl border border-border/60 bg-card/60 p-5 shadow-card transition hover:border-primary/40">
      <div className="flex items-center justify-between">
        <p className="text-xs uppercase tracking-[0.14em] text-muted-foreground">{label}</p>
        <Icon className="h-4 w-4 text-primary" />
      </div>
      <p className="mt-3 font-display text-2xl sm:text-3xl font-semibold tracking-tight">{value}</p>
      <p className="mt-1 text-xs text-muted-foreground">{hint}</p>
    </div>
  );
}

function FeatureCard({
  icon: Icon,
  title,
  description,
  to,
  cta,
}: {
  icon: typeof LineChartIcon;
  title: string;
  description: string;
  to: string;
  cta: string;
}) {
  return (
    <Link
      to={to as any}
      className="group rounded-2xl border border-border/60 bg-card/60 p-5 shadow-card hover:border-primary/40 transition flex flex-col"
    >
      <div className="flex items-center gap-3">
        <div className="grid h-9 w-9 place-items-center rounded-lg bg-primary/15 text-primary ring-1 ring-primary/30">
          <Icon className="h-4 w-4" />
        </div>
        <h3 className="text-sm font-semibold">{title}</h3>
      </div>
      <p className="mt-3 text-sm text-muted-foreground">{description}</p>
      <span className="mt-4 inline-flex items-center gap-1 text-xs text-primary group-hover:gap-2 transition-all">
        {cta} <ArrowRight className="h-3 w-3" />
      </span>
    </Link>
  );
}
