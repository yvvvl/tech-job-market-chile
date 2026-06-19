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

async function apiFetch<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export function getMarketOverview() {
  return apiFetch<MarketOverview>("/stats/overview");
}

export function getTechnologies() {
  return apiFetch<Technology[]>("/stats/technologies");
}

export function getRecommendations() {
  return apiFetch<RecommendationsResponse>("/recommendations");
}
