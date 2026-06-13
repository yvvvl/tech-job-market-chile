import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { ArrowUpRight, Search, TrendingUp, Users } from "lucide-react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader, Section } from "@/components/ui-kit/Section";
import { DarkTooltip } from "@/components/charts/ChartTooltip";
import { formatCLP, monthlyTrend, technologies, type Technology } from "@/lib/mockData";
import { cn } from "@/lib/utils";
import { useT } from "@/lib/i18n";

export const Route = createFileRoute("/explorer")({
  head: () => ({
    meta: [
      { title: "Technology Explorer — TechMarket CL" },
      {
        name: "description",
        content: "Search any technology and see its demand, trend and related stack in Chile.",
      },
    ],
  }),
  component: ExplorerPage,
});

function ExplorerPage() {
  const t = useT();
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Technology>(technologies[0]);

  const filtered = technologies.filter((tech) =>
    tech.name.toLowerCase().includes(query.toLowerCase()),
  );

  const trendData = monthlyTrend.map((m, i) => ({
    month: m.month,
    demand: Math.round((selected.demand / 12) * (0.85 + i * 0.025) * (1 + selected.trend / 200)),
  }));

  return (
    <AppShell>
      <PageHeader
        eyebrow={t("exp.eyebrow")}
        title={t("exp.title")}
        description={t("exp.desc")}
      />

      <div className="grid lg:grid-cols-[320px_1fr] gap-6">
        <div className="rounded-2xl border border-border/60 bg-card/50 p-4 shadow-card h-fit lg:sticky lg:top-24">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={t("exp.searchPlaceholder")}
              className="w-full rounded-lg border border-border bg-background/60 pl-9 pr-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
          </div>
          <div className="mt-4 max-h-[480px] overflow-y-auto pr-1 space-y-1">
            {filtered.length === 0 ? (
              <EmptyState query={query} />
            ) : (
              filtered.map((tech) => (
                <button
                  key={tech.name}
                  onClick={() => setSelected(tech)}
                  className={cn(
                    "w-full text-left px-3 py-2.5 rounded-lg border border-transparent transition flex items-center justify-between hover:bg-accent/40",
                    selected.name === tech.name && "border-primary/40 bg-primary/10",
                  )}
                >
                  <div>
                    <p className="text-sm font-medium">{tech.name}</p>
                    <p className="text-[11px] text-muted-foreground">{tech.category}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs font-mono">{tech.demand.toLocaleString()}</p>
                    <p
                      className={cn(
                        "text-[10px]",
                        tech.trend >= 0 ? "text-[color:var(--color-success)]" : "text-destructive",
                      )}
                    >
                      {tech.trend >= 0 ? "+" : ""}
                      {tech.trend}%
                    </p>
                  </div>
                </button>
              ))
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="rounded-2xl border border-border/60 bg-card/60 p-6 shadow-card">
            <div className="flex items-start justify-between flex-wrap gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.18em] text-primary">{selected.category}</p>
                <h2 className="mt-1 font-display text-3xl font-semibold tracking-tight">
                  {selected.name}
                </h2>
                <p className="mt-2 text-sm text-muted-foreground max-w-md">
                  {t("exp.subtitle")}
                </p>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <ScorePill label={t("exp.score.demand")} value={demandScore(selected)} />
                <ScorePill label={t("exp.score.trend")} value={selected.trend} accent={selected.trend >= 0} />
                <ScorePill label={t("exp.score.junior")} value={selected.juniorFriendly} suffix="%" />
              </div>
            </div>

            <div className="mt-6 grid sm:grid-cols-3 gap-4">
              <KV label={t("exp.kv.postings")} value={selected.demand.toLocaleString()} icon={<Users className="h-4 w-4" />} />
              <KV label={t("exp.kv.avgSalary")} value={formatCLP(selected.avgSalaryCLP)} icon={<ArrowUpRight className="h-4 w-4" />} />
              <KV label={t("exp.kv.momentum")} value={`${selected.trend > 0 ? "+" : ""}${selected.trend}% mo/mo`} icon={<TrendingUp className="h-4 w-4" />} />
            </div>
          </div>

          <Section title={t("exp.trend.title")} description={`${t("exp.trend.desc")} ${selected.name}`}>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData}>
                  <CartesianGrid stroke="var(--color-border)" vertical={false} />
                  <XAxis dataKey="month" stroke="var(--color-muted-foreground)" fontSize={11} tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--color-muted-foreground)" fontSize={11} tickLine={false} axisLine={false} />
                  <Tooltip content={<DarkTooltip />} />
                  <Line type="monotone" dataKey="demand" name={t("chart.postings")} stroke="var(--color-primary)" strokeWidth={2.5} dot={{ r: 3 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Section>

          <div className="grid sm:grid-cols-2 gap-6">
            <Section title={t("exp.related.title")} description={t("exp.related.desc")}>
              <div className="flex flex-wrap gap-2">
                {selected.related.map((r) => (
                  <span
                    key={r}
                    className="inline-flex items-center rounded-full border border-border/70 bg-background/60 px-3 py-1 text-xs text-muted-foreground"
                  >
                    {r}
                  </span>
                ))}
              </div>
            </Section>

            <Section title={t("exp.junior.title")} description={t("exp.junior.desc")}>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">{t("exp.junior.label")}</span>
                  <span className="font-mono">{selected.juniorFriendly}%</span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${selected.juniorFriendly}%`,
                      background: "var(--gradient-primary)",
                    }}
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  {t("exp.junior.summary.a")} {Math.round((selected.demand * selected.juniorFriendly) / 100).toLocaleString()} {t("exp.junior.summary.b")}
                </p>
              </div>
            </Section>
          </div>
        </div>
      </div>
    </AppShell>
  );
}

function demandScore(t: Technology) {
  const max = Math.max(...technologies.map((x) => x.demand));
  return Math.round((t.demand / max) * 100);
}

function ScorePill({
  label,
  value,
  suffix,
  accent,
}: {
  label: string;
  value: number;
  suffix?: string;
  accent?: boolean;
}) {
  return (
    <div className="rounded-xl border border-border/60 bg-background/60 px-3 py-2 text-center min-w-[88px]">
      <p className="text-[10px] uppercase tracking-[0.15em] text-muted-foreground">{label}</p>
      <p
        className={cn(
          "mt-1 font-display text-lg font-semibold",
          accent === true && "text-[color:var(--color-success)]",
          accent === false && "text-destructive",
        )}
      >
        {value > 0 && suffix === undefined && accent !== undefined ? "+" : ""}
        {value}
        {suffix ?? ""}
      </p>
    </div>
  );
}

function KV({ label, value, icon }: { label: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-border/60 bg-background/40 px-4 py-3">
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        <span className="text-primary">{icon}</span>
        {label}
      </div>
      <p className="mt-1 font-mono text-sm">{value}</p>
    </div>
  );
}

function EmptyState({ query }: { query: string }) {
  const t = useT();
  return (
    <div className="px-3 py-8 text-center">
      <Search className="mx-auto h-5 w-5 text-muted-foreground" />
      <p className="mt-2 text-sm font-medium">{t("exp.empty.title")}</p>
      <p className="text-xs text-muted-foreground">
        {t("exp.empty.desc")} "{query}".
      </p>
    </div>
  );
}
