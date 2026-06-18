import {
  createContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { I18nCtx, type Lang, type Dict, type Ctx } from "./i18n-context";

const en: Dict = {
  // Nav / shell
  "nav.overview": "Overview",
  "nav.dashboard": "Dashboard",
  "nav.explorer": "Explorer",
  "nav.recommendations": "Career Paths",
  "brand.tagline": "Job Intelligence",
  "cta.exploreInsights": "Explore Insights",
  "footer.copy": "Chilean tech job intelligence.",
  "footer.note": "Data updated weekly · Mock dataset for demo purposes",
  "lang.toggle": "ES",
  "lang.aria": "Switch language",

  // Landing
  "landing.badge": "Updated weekly",
  "landing.activePostings": "active postings",
  "landing.h1.a": "Discover what technologies",
  "landing.h1.b": "companies are hiring for in Chile.",
  "landing.subtitle":
    "A data-driven view of the Chilean tech job market — built for computer science students, data students, juniors and career switchers ready to make their next move.",
  "landing.cta.primary": "Explore Insights",
  "landing.cta.secondary": "See learning paths",
  "landing.chart.eyebrow": "Postings — last 12 months",
  "landing.chart.delta": "+18% YoY",
  "landing.overview.eyebrow": "Market overview",
  "landing.overview.title": "The Chilean tech market at a glance",
  "landing.overview.desc":
    "Aggregated signals from job boards, company career pages and ATS feeds across Chile.",
  "landing.demand.eyebrow": "Demand",
  "landing.demand.title": "Most demanded technologies",
  "landing.demand.desc":
    "Top 6 technologies by number of open postings this month.",
  "feat.junior.title": "Junior Opportunities",
  "feat.junior.desc":
    "2,180+ postings open to junior talent — sorted by accessibility, salary and growth.",
  "feat.junior.cta": "View junior jobs",
  "feat.salary.title": "Salary Insights",
  "feat.salary.desc":
    "Compare salary ranges by stack, seniority and city — calibrated for the Chilean market.",
  "feat.salary.cta": "Explore salaries",
  "feat.learn.title": "Learning Recommendations",
  "feat.learn.desc":
    "Personalized learning paths based on real demand signals — not opinions.",
  "feat.learn.cta": "See learning paths",
  "cta.section.title": "Make your next move with data on your side.",
  "cta.section.desc":
    "Open the full dashboard — explore demand, salaries and trends across the Chilean tech ecosystem.",
  "cta.section.btn": "Open Dashboard",

  // Stats
  "stat.totalJobs": "Total Jobs",
  "stat.companies": "Companies",
  "stat.technologies": "Technologies",
  "stat.cities": "Cities",
  "stat.hint.active": "Active postings",
  "stat.hint.hiring": "Hiring right now",
  "stat.hint.hiringMonth": "Hiring this month",
  "stat.hint.tracked": "Tracked weekly",
  "stat.hint.acrossChile": "Across Chile",
  "stat.vsLastMonth": "vs last month",

  // Dashboard
  "dash.eyebrow": "Dashboard",
  "dash.title": "Chilean tech market dashboard",
  "dash.desc":
    "Real-time view across postings, companies, cities and salaries.",
  "dash.topTech.title": "Most demanded technologies",
  "dash.topTech.desc": "Top 8 by number of active postings",
  "dash.category.title": "By category",
  "dash.category.desc": "Demand share across the stack",
  "dash.cities.title": "Postings by city",
  "dash.cities.desc": "Where the demand concentrates",
  "dash.seniority.title": "By seniority",
  "dash.seniority.desc": "Distribution of openings",
  "dash.salary.title": "Salary ranges (CLP, monthly)",
  "dash.salary.desc": "Distribution across postings",
  "dash.trend.title": "Monthly trend",
  "dash.trend.desc":
    "Postings volume and junior-friendly openings over the past 12 months",
  "chart.postings": "Postings",
  "chart.jobs": "Jobs",
  "chart.totalJobs": "Total jobs",
  "chart.juniorFriendly": "Junior-friendly",

  // Explorer
  "exp.eyebrow": "Technology Explorer",
  "exp.title": "Search any technology",
  "exp.desc":
    "Demand, trend, related skills and junior accessibility — for every tech in our index.",
  "exp.searchPlaceholder": "Try Python, React, AWS…",
  "exp.empty.title": "No matches",
  "exp.empty.desc": "No technologies match",
  "exp.subtitle":
    "Aggregated demand and trend signals from active Chilean job postings.",
  "exp.score.demand": "Demand",
  "exp.score.trend": "Trend",
  "exp.score.junior": "Junior friendly",
  "exp.kv.postings": "Open postings",
  "exp.kv.avgSalary": "Avg salary",
  "exp.kv.momentum": "Momentum",
  "exp.trend.title": "Demand trend",
  "exp.trend.desc": "Monthly demand for",
  "exp.related.title": "Related technologies",
  "exp.related.desc": "Commonly required alongside",
  "exp.junior.title": "Junior opportunities",
  "exp.junior.desc": "Share of postings open to junior talent",
  "exp.junior.label": "Junior-friendly",
  "exp.junior.summary.a": "Roughly",
  "exp.junior.summary.b": "postings open to junior candidates.",

  // Recommendations
  "rec.eyebrow": "Career recommendations",
  "rec.title": "Learning paths backed by real demand",
  "rec.desc":
    "Roadmaps assembled from current Chilean job postings — not opinions or rankings.",
  "rec.path": "Path",
  "rec.demandScore": "Demand score",
  "rec.indicator.demand": "Market demand",
  "rec.indicator.junior": "Junior accessibility",
  "rec.stack": "Suggested stack",
  "rec.weeks": "weeks",
  "rec.exploreStack": "Explore stack",
  "rec.suggested.title": "Suggested technologies for juniors",
  "rec.suggested.desc":
    "Highest combined score of demand and junior accessibility — great places to start.",
  "rec.juniorSuffix": "junior",

  // Learning paths
  "path.frontend.title": "Frontend Engineer",
  "path.frontend.desc":
    "Build modern interfaces for Chilean fintech and SaaS companies.",
  "path.backend.title": "Backend Engineer",
  "path.backend.desc":
    "Power APIs and data pipelines for high-growth startups.",
  "path.data.title": "Data Analyst",
  "path.data.desc":
    "Turn raw data into business decisions across retail and banking.",
  "path.cloud.title": "Cloud & DevOps",
  "path.cloud.desc": "Operate cloud infrastructure for enterprise migrations.",
};

const es: Dict = {
  "nav.overview": "Inicio",
  "nav.dashboard": "Panel",
  "nav.explorer": "Explorador",
  "nav.recommendations": "Rutas de Carrera",
  "brand.tagline": "Inteligencia Laboral",
  "cta.exploreInsights": "Explorar Datos",
  "footer.copy": "Inteligencia del mercado laboral tech chileno.",
  "footer.note": "Datos actualizados semanalmente · Datos simulados para demo",
  "lang.toggle": "EN",
  "lang.aria": "Cambiar idioma",

  "landing.badge": "Actualizado semanalmente",
  "landing.activePostings": "ofertas activas",
  "landing.h1.a": "Descubre qué tecnologías",
  "landing.h1.b": "están contratando las empresas en Chile.",
  "landing.subtitle":
    "Una visión basada en datos del mercado laboral tech chileno — pensada para estudiantes de informática, ciencia de datos, juniors y quienes cambian de carrera y buscan su próximo paso.",
  "landing.cta.primary": "Explorar Datos",
  "landing.cta.secondary": "Ver rutas de aprendizaje",
  "landing.chart.eyebrow": "Ofertas — últimos 12 meses",
  "landing.chart.delta": "+18% interanual",
  "landing.overview.eyebrow": "Resumen del mercado",
  "landing.overview.title": "El mercado tech chileno de un vistazo",
  "landing.overview.desc":
    "Señales agregadas desde portales de empleo, páginas de carrera y ATS en todo Chile.",
  "landing.demand.eyebrow": "Demanda",
  "landing.demand.title": "Tecnologías más demandadas",
  "landing.demand.desc":
    "Top 6 de tecnologías por número de ofertas abiertas este mes.",
  "feat.junior.title": "Oportunidades Junior",
  "feat.junior.desc":
    "Más de 2.180 ofertas abiertas a talento junior — ordenadas por accesibilidad, salario y crecimiento.",
  "feat.junior.cta": "Ver empleos junior",
  "feat.salary.title": "Datos de Salarios",
  "feat.salary.desc":
    "Compara rangos salariales por stack, seniority y ciudad — calibrado al mercado chileno.",
  "feat.salary.cta": "Explorar salarios",
  "feat.learn.title": "Recomendaciones de Aprendizaje",
  "feat.learn.desc":
    "Rutas de aprendizaje personalizadas basadas en demanda real — no en opiniones.",
  "feat.learn.cta": "Ver rutas de aprendizaje",
  "cta.section.title": "Toma tu próxima decisión con datos de tu lado.",
  "cta.section.desc":
    "Abre el panel completo — explora demanda, salarios y tendencias del ecosistema tech chileno.",
  "cta.section.btn": "Abrir Panel",

  "stat.totalJobs": "Empleos Totales",
  "stat.companies": "Empresas",
  "stat.technologies": "Tecnologías",
  "stat.cities": "Ciudades",
  "stat.hint.active": "Ofertas activas",
  "stat.hint.hiring": "Contratando ahora",
  "stat.hint.hiringMonth": "Contratando este mes",
  "stat.hint.tracked": "Monitoreadas semanalmente",
  "stat.hint.acrossChile": "En todo Chile",
  "stat.vsLastMonth": "vs mes anterior",

  "dash.eyebrow": "Panel",
  "dash.title": "Panel del mercado tech chileno",
  "dash.desc":
    "Vista en tiempo real de ofertas, empresas, ciudades y salarios.",
  "dash.topTech.title": "Tecnologías más demandadas",
  "dash.topTech.desc": "Top 8 por número de ofertas activas",
  "dash.category.title": "Por categoría",
  "dash.category.desc": "Distribución de demanda en el stack",
  "dash.cities.title": "Ofertas por ciudad",
  "dash.cities.desc": "Dónde se concentra la demanda",
  "dash.seniority.title": "Por seniority",
  "dash.seniority.desc": "Distribución de vacantes",
  "dash.salary.title": "Rangos salariales (CLP, mensual)",
  "dash.salary.desc": "Distribución entre ofertas",
  "dash.trend.title": "Tendencia mensual",
  "dash.trend.desc":
    "Volumen de ofertas y vacantes junior-friendly en los últimos 12 meses",
  "chart.postings": "Ofertas",
  "chart.jobs": "Empleos",
  "chart.totalJobs": "Empleos totales",
  "chart.juniorFriendly": "Junior-friendly",

  "exp.eyebrow": "Explorador de Tecnologías",
  "exp.title": "Busca cualquier tecnología",
  "exp.desc":
    "Demanda, tendencia, skills relacionadas y accesibilidad junior — para cada tecnología.",
  "exp.searchPlaceholder": "Prueba Python, React, AWS…",
  "exp.empty.title": "Sin resultados",
  "exp.empty.desc": "Ninguna tecnología coincide con",
  "exp.subtitle":
    "Demanda y tendencia agregadas desde ofertas activas en Chile.",
  "exp.score.demand": "Demanda",
  "exp.score.trend": "Tendencia",
  "exp.score.junior": "Apto junior",
  "exp.kv.postings": "Ofertas abiertas",
  "exp.kv.avgSalary": "Salario promedio",
  "exp.kv.momentum": "Momentum",
  "exp.trend.title": "Tendencia de demanda",
  "exp.trend.desc": "Demanda mensual para",
  "exp.related.title": "Tecnologías relacionadas",
  "exp.related.desc": "Frecuentemente requeridas junto a esta",
  "exp.junior.title": "Oportunidades para juniors",
  "exp.junior.desc": "Porcentaje de ofertas abiertas a talento junior",
  "exp.junior.label": "Apto junior",
  "exp.junior.summary.a": "Aproximadamente",
  "exp.junior.summary.b": "ofertas abiertas a candidatos junior.",

  "rec.eyebrow": "Recomendaciones de carrera",
  "rec.title": "Rutas de aprendizaje respaldadas por demanda real",
  "rec.desc":
    "Roadmaps construidos a partir de ofertas reales en Chile — no opiniones ni rankings.",
  "rec.path": "Ruta",
  "rec.demandScore": "Score de demanda",
  "rec.indicator.demand": "Demanda del mercado",
  "rec.indicator.junior": "Accesibilidad junior",
  "rec.stack": "Stack sugerido",
  "rec.weeks": "semanas",
  "rec.exploreStack": "Explorar stack",
  "rec.suggested.title": "Tecnologías sugeridas para juniors",
  "rec.suggested.desc":
    "Mayor score combinado de demanda y accesibilidad junior — un gran punto de partida.",
  "rec.juniorSuffix": "junior",

  "path.frontend.title": "Frontend Engineer",
  "path.frontend.desc":
    "Construye interfaces modernas para fintech y SaaS chilenas.",
  "path.backend.title": "Backend Engineer",
  "path.backend.desc":
    "Potencia APIs y pipelines de datos para startups en crecimiento.",
  "path.data.title": "Analista de Datos",
  "path.data.desc":
    "Convierte datos crudos en decisiones de negocio en retail y banca.",
  "path.cloud.title": "Cloud & DevOps",
  "path.cloud.desc":
    "Opera infraestructura cloud para migraciones empresariales.",
};

const dicts: Record<Lang, Dict> = { en, es };

type Ctx = { lang: Lang; setLang: (l: Lang) => void; t: (k: string) => string };
const I18nCtx = createContext<Ctx>({
  lang: "en",
  setLang: () => {},
  t: (k) => k,
});

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("en");

  useEffect(() => {
    try {
      const stored = localStorage.getItem("lang") as Lang | null;
      if (stored === "en" || stored === "es") {
        setLangState(stored);
      }
    } catch {
      console.warn("Could not read language from localStorage.");
    }
  }, []);

  const setLang = (l: Lang) => {
    setLangState(l);
    try {
      localStorage.setItem("lang", l);
    } catch {
      console.warn("Could not save language to localStorage.");
    }
  };

  const value = useMemo<Ctx>(
    () => ({
      lang,
      setLang,
      t: (k: string) => dicts[lang][k] ?? dicts.en[k] ?? k,
    }),
    [lang],
  );

  return <I18nCtx.Provider value={value}>{children}</I18nCtx.Provider>;
}
