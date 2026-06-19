export type Technology = {
  name: string;
  category:
    | "Language"
    | "Frontend"
    | "Backend"
    | "Database"
    | "Cloud"
    | "DevOps"
    | "Data";
  demand: number; // # of postings
  trend: number; // % change vs last month
  juniorFriendly: number; // % of postings open to junior
  avgSalaryCLP: number; // monthly net CLP
  related: string[];
};

export const technologies: Technology[] = [
  {
    name: "Python",
    category: "Language",
    demand: 1820,
    trend: 12,
    juniorFriendly: 38,
    avgSalaryCLP: 2_200_000,
    related: ["Django", "FastAPI", "SQL", "AWS"],
  },
  {
    name: "JavaScript",
    category: "Language",
    demand: 1640,
    trend: 6,
    juniorFriendly: 45,
    avgSalaryCLP: 1_900_000,
    related: ["React", "Node.js", "TypeScript"],
  },
  {
    name: "TypeScript",
    category: "Language",
    demand: 1380,
    trend: 22,
    juniorFriendly: 30,
    avgSalaryCLP: 2_350_000,
    related: ["React", "Node.js", "Next.js"],
  },
  {
    name: "Java",
    category: "Language",
    demand: 1240,
    trend: -3,
    juniorFriendly: 28,
    avgSalaryCLP: 2_500_000,
    related: ["Spring", "SQL", "AWS"],
  },
  {
    name: "React",
    category: "Frontend",
    demand: 1510,
    trend: 18,
    juniorFriendly: 42,
    avgSalaryCLP: 2_150_000,
    related: ["TypeScript", "Next.js", "Redux"],
  },
  {
    name: "Node.js",
    category: "Backend",
    demand: 1120,
    trend: 14,
    juniorFriendly: 35,
    avgSalaryCLP: 2_300_000,
    related: ["JavaScript", "Express", "PostgreSQL"],
  },
  {
    name: "SQL",
    category: "Database",
    demand: 1980,
    trend: 4,
    juniorFriendly: 55,
    avgSalaryCLP: 1_850_000,
    related: ["PostgreSQL", "MySQL", "Python"],
  },
  {
    name: "PostgreSQL",
    category: "Database",
    demand: 870,
    trend: 11,
    juniorFriendly: 32,
    avgSalaryCLP: 2_200_000,
    related: ["SQL", "Node.js", "Django"],
  },
  {
    name: "AWS",
    category: "Cloud",
    demand: 1320,
    trend: 16,
    juniorFriendly: 18,
    avgSalaryCLP: 2_900_000,
    related: ["Docker", "Terraform", "Python"],
  },
  {
    name: "Docker",
    category: "DevOps",
    demand: 990,
    trend: 9,
    juniorFriendly: 22,
    avgSalaryCLP: 2_700_000,
    related: ["Kubernetes", "AWS", "CI/CD"],
  },
  {
    name: "Kubernetes",
    category: "DevOps",
    demand: 540,
    trend: 20,
    juniorFriendly: 8,
    avgSalaryCLP: 3_400_000,
    related: ["Docker", "AWS", "Terraform"],
  },
  {
    name: "Power BI",
    category: "Data",
    demand: 720,
    trend: 7,
    juniorFriendly: 48,
    avgSalaryCLP: 1_800_000,
    related: ["SQL", "Excel", "Python"],
  },
  {
    name: "Pandas",
    category: "Data",
    demand: 610,
    trend: 13,
    juniorFriendly: 40,
    avgSalaryCLP: 2_000_000,
    related: ["Python", "SQL", "Jupyter"],
  },
];

export const stats = {
  totalJobs: 8420,
  companies: 612,
  technologies: 148,
  cities: 12,
};

export const monthlyTrend = [
  { month: "Jan", jobs: 5200, junior: 1100 },
  { month: "Feb", jobs: 5680, junior: 1240 },
  { month: "Mar", jobs: 6010, junior: 1380 },
  { month: "Apr", jobs: 6420, junior: 1490 },
  { month: "May", jobs: 6890, junior: 1620 },
  { month: "Jun", jobs: 7250, junior: 1780 },
  { month: "Jul", jobs: 7610, junior: 1840 },
  { month: "Aug", jobs: 7980, junior: 1950 },
  { month: "Sep", jobs: 8120, junior: 2010 },
  { month: "Oct", jobs: 8290, junior: 2080 },
  { month: "Nov", jobs: 8350, junior: 2120 },
  { month: "Dec", jobs: 8420, junior: 2180 },
];

export const cities = [
  { city: "Santiago", jobs: 6120 },
  { city: "Valparaíso", jobs: 680 },
  { city: "Concepción", jobs: 540 },
  { city: "Viña del Mar", jobs: 320 },
  { city: "Antofagasta", jobs: 210 },
  { city: "La Serena", jobs: 180 },
  { city: "Remote (Chile)", jobs: 370 },
];

export const seniority = [
  { level: "Junior", count: 2180, fill: "var(--color-chart-2)" },
  { level: "Semi-Senior", count: 3260, fill: "var(--color-chart-1)" },
  { level: "Senior", count: 2410, fill: "var(--color-chart-3)" },
  { level: "Lead / Staff", count: 570, fill: "var(--color-chart-4)" },
];

export const salaryRanges = [
  { range: "< 1M", count: 420 },
  { range: "1M – 1.5M", count: 1180 },
  { range: "1.5M – 2M", count: 2240 },
  { range: "2M – 2.5M", count: 1980 },
  { range: "2.5M – 3M", count: 1340 },
  { range: "3M – 4M", count: 820 },
  { range: "> 4M", count: 440 },
];

export const categoryBreakdown = (() => {
  const map = new Map<string, number>();
  technologies.forEach((t) =>
    map.set(t.category, (map.get(t.category) ?? 0) + t.demand),
  );
  return Array.from(map, ([category, demand]) => ({ category, demand })).sort(
    (a, b) => b.demand - a.demand,
  );
})();

export const learningPaths = [
  {
    title: "Frontend Engineer",
    description:
      "Build modern interfaces for Chilean fintech and SaaS companies.",
    techs: ["TypeScript", "React", "Next.js", "TailwindCSS"],
    demandScore: 92,
    juniorScore: 88,
    timeWeeks: 16,
  },
  {
    title: "Backend Engineer",
    description: "Power APIs and data pipelines for high-growth startups.",
    techs: ["Python", "FastAPI", "PostgreSQL", "Docker"],
    demandScore: 95,
    juniorScore: 74,
    timeWeeks: 20,
  },
  {
    title: "Data Analyst",
    description:
      "Turn raw data into business decisions across retail and banking.",
    techs: ["SQL", "Python", "Pandas", "Power BI"],
    demandScore: 87,
    juniorScore: 90,
    timeWeeks: 14,
  },
  {
    title: "Cloud & DevOps",
    description: "Operate cloud infrastructure for enterprise migrations.",
    techs: ["AWS", "Docker", "Kubernetes", "Terraform"],
    demandScore: 84,
    juniorScore: 35,
    timeWeeks: 24,
  },
];

export const formatCLP = (value: number) =>
  new Intl.NumberFormat("es-CL", {
    style: "currency",
    currency: "CLP",
    maximumFractionDigits: 0,
  }).format(value);

export const formatNumber = (value: number) =>
  new Intl.NumberFormat("en-US").format(value);

export const delay = <T>(data: T, ms = 350) =>
  new Promise<T>((resolve) => setTimeout(() => resolve(data), ms));
