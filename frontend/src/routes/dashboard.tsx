import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Briefcase, Building2, Cpu, MapPin } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader, Section } from "@/components/ui-kit/Section";
import { StatCard } from "@/components/ui-kit/StatCard";
import { DarkTooltip } from "@/components/charts/ChartTooltip";
import { useT } from "@/lib/i18n-hooks";
import { formatNumber } from "@/lib/mockData";
import { getMarketOverview } from "@/lib/api/market";

export const Route = createFileRoute("/dashboard")({
  head: () => ({
    meta: [
      { title: "Dashboard — TechMarket CL" },
      {
        name: "description",
        content:
          "Live dashboard of the Chilean tech job market: demand, salaries, seniority and city breakdowns.",
      },
    ],
  }),
  component: DashboardPage,
});

const CHART_COLORS = [
  "var(--color-chart-1)",
  "var(--color-chart-2)",
  "var(--color-chart-3)",
  "var(--color-chart-4)",
  "var(--color-chart-5)",
];

function DashboardPage() {
  const t = useT();
  const overview = useQuery({
    queryKey: ["overview"],
    queryFn: getMarketOverview,
  });

  if (overview.isLoading || !overview.data) {
    return (
      <AppShell>
        <PageHeader
          eyebrow={t("dash.eyebrow")}
          title={t("dash.title")}
          description={t("dash.desc")}
        />
        <SkeletonGrid />
      </AppShell>
    );
  }

  const d = overview.data;
  const topTechs = d.technologies.slice(0, 8);

  return (
    <AppShell>
      <PageHeader
        eyebrow={t("dash.eyebrow")}
        title={t("dash.title")}
        description={t("dash.desc")}
      />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label={t("stat.totalJobs")}
          value={formatNumber(d.stats.totalJobs)}
          delta={8}
          icon={Briefcase}
          hint={t("stat.hint.active")}
        />
        <StatCard
          label={t("stat.companies")}
          value={formatNumber(d.stats.companies)}
          delta={4}
          icon={Building2}
          hint={t("stat.hint.hiringMonth")}
        />
        <StatCard
          label={t("stat.technologies")}
          value={formatNumber(d.stats.technologies)}
          delta={2}
          icon={Cpu}
          hint={t("stat.hint.tracked")}
        />
        <StatCard
          label={t("stat.cities")}
          value={formatNumber(d.stats.cities)}
          icon={MapPin}
          hint={t("stat.hint.acrossChile")}
        />
      </div>

      <div className="mt-6 grid lg:grid-cols-3 gap-6">
        <Section
          title={t("dash.topTech.title")}
          description={t("dash.topTech.desc")}
          className="lg:col-span-2"
        >
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topTechs}>
                <CartesianGrid stroke="var(--color-border)" vertical={false} />
                <XAxis
                  dataKey="name"
                  stroke="var(--color-muted-foreground)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="var(--color-muted-foreground)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip
                  content={<DarkTooltip />}
                  cursor={{ fill: "var(--color-muted)", opacity: 0.25 }}
                />
                <Bar
                  dataKey="demand"
                  name={t("chart.postings")}
                  radius={[6, 6, 0, 0]}
                >
                  {topTechs.map((_, i) => (
                    <Cell
                      key={i}
                      fill={CHART_COLORS[i % CHART_COLORS.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Section>

        <Section
          title={t("dash.category.title")}
          description={t("dash.category.desc")}
        >
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={d.categoryBreakdown}
                  dataKey="demand"
                  nameKey="category"
                  innerRadius={55}
                  outerRadius={95}
                  paddingAngle={3}
                  stroke="var(--color-background)"
                  strokeWidth={2}
                >
                  {d.categoryBreakdown.map((_, i) => (
                    <Cell
                      key={i}
                      fill={CHART_COLORS[i % CHART_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip content={<DarkTooltip />} />
                <Legend
                  verticalAlign="bottom"
                  iconType="circle"
                  wrapperStyle={{
                    fontSize: 11,
                    color: "var(--color-muted-foreground)",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Section>
      </div>

      <div className="mt-6 grid lg:grid-cols-3 gap-6">
        <Section
          title={t("dash.cities.title")}
          description={t("dash.cities.desc")}
        >
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={d.cities} layout="vertical">
                <CartesianGrid
                  stroke="var(--color-border)"
                  horizontal={false}
                />
                <XAxis
                  type="number"
                  stroke="var(--color-muted-foreground)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  type="category"
                  dataKey="city"
                  stroke="var(--color-muted-foreground)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                  width={110}
                />
                <Tooltip
                  content={<DarkTooltip />}
                  cursor={{ fill: "var(--color-muted)", opacity: 0.25 }}
                />
                <Bar
                  dataKey="jobs"
                  name={t("chart.jobs")}
                  fill="var(--color-chart-3)"
                  radius={[0, 6, 6, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Section>

        <Section
          title={t("dash.seniority.title")}
          description={t("dash.seniority.desc")}
        >
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={d.seniority}
                  dataKey="count"
                  nameKey="level"
                  outerRadius={95}
                  stroke="var(--color-background)"
                  strokeWidth={2}
                  label={{
                    fontSize: 11,
                    fill: "var(--color-muted-foreground)",
                  }}
                >
                  {d.seniority.map((_, i) => (
                    <Cell
                      key={i}
                      fill={CHART_COLORS[i % CHART_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip content={<DarkTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Section>

        <Section
          title={t("dash.salary.title")}
          description={t("dash.salary.desc")}
        >
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={d.salaryRanges}>
                <CartesianGrid stroke="var(--color-border)" vertical={false} />
                <XAxis
                  dataKey="range"
                  stroke="var(--color-muted-foreground)"
                  fontSize={10}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="var(--color-muted-foreground)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip
                  content={<DarkTooltip />}
                  cursor={{ fill: "var(--color-muted)", opacity: 0.25 }}
                />
                <Bar
                  dataKey="count"
                  name={t("chart.postings")}
                  fill="var(--color-chart-2)"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Section>
      </div>

      <div className="mt-6">
        <Section
          title={t("dash.trend.title")}
          description={t("dash.trend.desc")}
        >
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={d.monthlyTrend}>
                <CartesianGrid stroke="var(--color-border)" vertical={false} />
                <XAxis
                  dataKey="month"
                  stroke="var(--color-muted-foreground)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="var(--color-muted-foreground)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip content={<DarkTooltip />} />
                <Legend
                  wrapperStyle={{
                    fontSize: 12,
                    color: "var(--color-muted-foreground)",
                  }}
                  iconType="circle"
                />
                <Line
                  type="monotone"
                  dataKey="jobs"
                  name={t("chart.totalJobs")}
                  stroke="var(--color-chart-1)"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
                <Line
                  type="monotone"
                  dataKey="junior"
                  name={t("chart.juniorFriendly")}
                  stroke="var(--color-chart-2)"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Section>
      </div>
    </AppShell>
  );
}

function SkeletonGrid() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className="h-32 rounded-2xl border border-border/60 bg-card/40 animate-pulse"
          />
        ))}
      </div>
      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 h-96 rounded-2xl border border-border/60 bg-card/40 animate-pulse" />
        <div className="h-96 rounded-2xl border border-border/60 bg-card/40 animate-pulse" />
      </div>
    </div>
  );
}
