import {
  categoryBreakdown as demoCategoryBreakdown,
  cities as demoCities,
  delay,
  learningPaths as demoLearningPaths,
  monthlyTrend as demoMonthlyTrend,
  salaryRanges as demoSalaryRanges,
  seniority as demoSeniority,
  stats as demoStats,
  technologies as demoTechnologies,
} from "@/lib/mockData";

export type Technology = {
  name: string;
  category:
    | "Language"
    | "Frontend"
    | "Backend"
    | "Database"
    | "Cloud"
    | "DevOps"
    | "Data"
    | string;
  demand: number;
  trend: number;
  juniorFriendly: number;
  avgSalaryCLP: number;
  related: string[];
};

export type MarketOverview = {
  stats: {
    totalJobs: number;
    companies: number;
    technologies: number;
    cities: number;
  };
  monthlyTrend: {
    month: string;
    jobs: number;
    junior: number;
  }[];
  technologies: Technology[];
  categoryBreakdown: {
    category: string;
    demand: number;
  }[];
  cities: {
    city: string;
    jobs: number;
  }[];
  seniority: {
    level: string;
    count: number;
    fill: string;
  }[];
  salaryRanges: {
    range: string;
    count: number;
  }[];
};

export type LearningPath = {
  title: string;
  description: string;
  techs: string[];
  demandScore: number;
  juniorScore: number;
  timeWeeks: number;
  totalDemand: number;
  avgSalaryCLP: number;
};

export type RecommendationsResponse = {
  learningPaths: LearningPath[];
  suggested: Technology[];
  metadata: {
    totalTechnologies: number;
    totalPaths: number;
    source: string;
  };
};

const API_BASE_URL =
  import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";
const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === "true";
const API_FALLBACK_ENABLED = import.meta.env.VITE_API_FALLBACK === "true";

const demoOverview: MarketOverview = {
  stats: demoStats,
  monthlyTrend: demoMonthlyTrend,
  technologies: demoTechnologies,
  categoryBreakdown: demoCategoryBreakdown,
  cities: demoCities,
  seniority: demoSeniority,
  salaryRanges: demoSalaryRanges,
};

const demoRecommendations: RecommendationsResponse = {
  learningPaths: demoLearningPaths.map((path) => {
    const matchingTechnologies = demoTechnologies.filter((technology) =>
      path.techs.includes(technology.name),
    );
    const totalDemand = matchingTechnologies.reduce(
      (total, technology) => total + technology.demand,
      0,
    );
    const avgSalaryCLP = matchingTechnologies.length
      ? Math.round(
          matchingTechnologies.reduce(
            (total, technology) => total + technology.avgSalaryCLP,
            0,
          ) / matchingTechnologies.length,
        )
      : 0;

    return {
      ...path,
      totalDemand,
      avgSalaryCLP,
    };
  }),
  suggested: [...demoTechnologies]
    .sort(
      (a, b) =>
        b.demand + b.juniorFriendly * 20 - (a.demand + a.juniorFriendly * 20),
    )
    .slice(0, 6),
  metadata: {
    totalTechnologies: demoTechnologies.length,
    totalPaths: demoLearningPaths.length,
    source: "versioned demo dataset",
  },
};

async function apiFetch<T>(path: string, demoData: T): Promise<T> {
  if (DEMO_MODE) {
    return delay(demoData, 250);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${path}`);

    if (!response.ok) {
      throw new Error(`API error ${response.status}: ${response.statusText}`);
    }

    return response.json() as Promise<T>;
  } catch (error) {
    if (API_FALLBACK_ENABLED) {
      console.warn(`API unavailable for ${path}; using demo data.`, error);
      return delay(demoData, 150);
    }

    throw error;
  }
}

export function getMarketOverview() {
  return apiFetch<MarketOverview>("/stats/overview", demoOverview);
}

export function getTechnologies() {
  return apiFetch<Technology[]>(
    "/stats/technologies",
    demoOverview.technologies,
  );
}

export function getRecommendations() {
  return apiFetch<RecommendationsResponse>(
    "/recommendations",
    demoRecommendations,
  );
}
