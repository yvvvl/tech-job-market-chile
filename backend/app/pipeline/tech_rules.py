import re
from collections import Counter


TECHNOLOGIES: dict[str, str] = {
    "Python": "Language",
    "JavaScript": "Language",
    "TypeScript": "Language",
    "Java": "Language",
    "C#": "Language",
    "PHP": "Language",
    "React": "Frontend",
    "Next.js": "Frontend",
    "Vue": "Frontend",
    "Angular": "Frontend",
    "TailwindCSS": "Frontend",
    "HTML": "Frontend",
    "CSS": "Frontend",
    "Node.js": "Backend",
    "Express": "Backend",
    "FastAPI": "Backend",
    "Django": "Backend",
    "Flask": "Backend",
    "Spring Boot": "Backend",
    "Laravel": "Backend",
    "SQL": "Database",
    "PostgreSQL": "Database",
    "MySQL": "Database",
    "MongoDB": "Database",
    "Power BI": "Data",
    "Excel": "Data",
    "Pandas": "Data",
    "NumPy": "Data",
    "Scikit-learn": "Data",
    "Machine Learning": "Data",
    "Docker": "DevOps",
    "Kubernetes": "DevOps",
    "Git": "DevOps",
    "GitHub": "DevOps",
    "CI/CD": "DevOps",
    "Terraform": "DevOps",
    "AWS": "Cloud",
    "Azure": "Cloud",
    "GCP": "Cloud",
}

ALIASES: dict[str, str] = {
    "react.js": "React",
    "reactjs": "React",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "cicd": "CI/CD",
    "ci/cd": "CI/CD",
    "tailwind": "TailwindCSS",
    "tailwind css": "TailwindCSS",
    "springboot": "Spring Boot",
    "spring boot": "Spring Boot",
}

for technology_name in list(TECHNOLOGIES.keys()):
    ALIASES.setdefault(technology_name.lower(), technology_name)


def extract_technologies(text: str) -> list[str]:
    if not text:
        return []

    found: set[str] = set()
    sorted_aliases = sorted(ALIASES.items(), key=lambda item: len(item[0]), reverse=True)

    for alias, canonical in sorted_aliases:
        pattern = rf"(?<![A-Za-z0-9_+#.]){re.escape(alias)}(?![A-Za-z0-9_+#.])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.add(canonical)

    return sorted(found)


def infer_seniority(title: str, description: str, fallback: str | None = None) -> str:
    text = f"{title} {description}".lower()

    if any(word in text for word in ["trainee", "práctica", "practica", "intern", "sin experiencia"]):
        return "trainee"
    if any(word in text for word in ["junior", "jr", "recién egresado", "recien egresado"]):
        return "junior"
    if any(word in text for word in ["semi senior", "semisenior", "ssr", "semi-senior"]):
        return "semi_senior"
    if any(word in text for word in ["senior", "sr", "lead", "staff", "principal", "arquitecto"]):
        return "senior"

    return clean_value(fallback) or "unknown"


def infer_modality(title: str, description: str, fallback: str | None = None) -> str:
    text = f"{title} {description} {fallback or ''}".lower()

    if any(word in text for word in ["remoto", "remote", "teletrabajo", "home office"]):
        return "remoto"
    if any(word in text for word in ["híbrido", "hibrido", "hybrid"]):
        return "hibrido"
    if any(word in text for word in ["presencial", "oficina", "onsite", "on-site"]):
        return "presencial"

    return clean_value(fallback) or "unknown"


def infer_job_category(title: str, description: str, technologies: list[str]) -> str:
    text = f"{title} {description}".lower()

    direct_rules = [
        ("backend", ["backend", "back-end", "api", "server"]),
        ("frontend", ["frontend", "front-end", "ui", "interfaz"]),
        ("fullstack", ["fullstack", "full-stack", "full stack"]),
        ("data", ["data", "datos", "analista", "analytics", "machine learning", "bi"]),
        ("devops", ["devops", "sre", "cloud", "infraestructura"]),
        ("qa", ["qa", "tester", "testing", "quality assurance"]),
    ]

    for category, keywords in direct_rules:
        if any(keyword in text for keyword in keywords):
            return category

    category_counter: Counter[str] = Counter()
    mapping = {
        "Frontend": "frontend",
        "Backend": "backend",
        "Data": "data",
        "DevOps": "devops",
        "Cloud": "devops",
        "Database": "backend",
        "Language": "backend",
    }

    for tech in technologies:
        tech_category = TECHNOLOGIES.get(tech)
        if tech_category in mapping:
            category_counter[mapping[tech_category]] += 1

    if category_counter:
        return category_counter.most_common(1)[0][0]

    return "other"


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().lower().replace(" ", "_").replace("-", "_")
    return cleaned or None