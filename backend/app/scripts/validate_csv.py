import argparse
import csv
import re
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

REQUIRED_COLUMNS = {
    "source",
    "source_url",
    "title",
    "company",
    "city",
    "region",
    "modality",
    "seniority",
    "category",
    "description",
    "technologies_raw",
    "salary_min",
    "salary_max",
    "salary_currency",
    "published_at",
    "collected_at",
}

REQUIRED_VALUE_COLUMNS = {
    "source",
    "title",
    "company",
    "description",
    "technologies_raw",
    "collected_at",
}

VALID_MODALITIES = {
    "remoto",
    "remote",
    "hibrido",
    "híbrido",
    "presencial",
    "unknown",
}

VALID_SENIORITIES = {
    "trainee",
    "junior",
    "semi_senior",
    "semi senior",
    "semisenior",
    "senior",
    "lead",
    "principal",
    "unknown",
}

VALID_CATEGORIES = {
    "backend",
    "frontend",
    "fullstack",
    "data",
    "devops",
    "qa",
    "security",
    "support",
    "management",
    "mobile",
    "cloud",
    "other",
}

VALID_CURRENCIES = {
    "CLP",
    "USD",
    "UF",
    "",
}

TECH_SPLIT_RE = re.compile(r"[;,\n|]+")


def clean_text(value: str | None) -> str:
    if value is None:
        return ""

    return value.strip()


def normalize_token(value: str | None) -> str:
    cleaned = clean_text(value)

    return (
        cleaned.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("-", "_")
        .replace(" ", "_")
    )


def parse_date(value: str | None) -> date | None:
    cleaned = clean_text(value)

    if not cleaned:
        return None

    try:
        return date.fromisoformat(cleaned)
    except ValueError as err:
        raise ValueError("Debe tener formato YYYY-MM-DD.") from err


def parse_int(value: str | None) -> int | None:
    cleaned = clean_text(value)

    if not cleaned:
        return None

    normalized = (
        cleaned.replace(".", "")
        .replace(",", "")
        .replace("$", "")
        .replace("CLP", "")
        .replace("USD", "")
        .replace("UF", "")
        .strip()
    )

    if not normalized:
        return None

    if not normalized.isdigit():
        raise ValueError(
            "Debe ser un número entero. "
            "Si aparece texto aquí, probablemente el CSV está desalineado "
            "por una coma sin comillas."
        )

    return int(normalized)


def split_technologies(value: str | None) -> list[str]:
    cleaned = clean_text(value)

    if not cleaned:
        return []

    technologies = []

    for part in TECH_SPLIT_RE.split(cleaned):
        tech = part.strip().strip('"').strip("'").strip()

        if tech:
            technologies.append(tech)

    return sorted(set(technologies))


def format_issue(level: str, line: int | str, column: str, message: str, value: str = "") -> str:
    location = f"línea {line}" if line else "archivo"

    if value:
        return f"[{level}] {location} | {column}: {message} Valor: {value}"

    return f"[{level}] {location} | {column}: {message}"


def validate_headers(headers: Sequence[str] | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if headers is None:
        errors.append(format_issue("ERROR", "", "headers", "El CSV no tiene encabezados."))
        return errors, warnings

    normalized_headers = [header.strip() for header in headers]
    missing = REQUIRED_COLUMNS - set(normalized_headers)
    extra = set(normalized_headers) - REQUIRED_COLUMNS

    duplicated = {header for header in normalized_headers if normalized_headers.count(header) > 1}

    if missing:
        errors.append(
            format_issue(
                "ERROR",
                "",
                "headers",
                "Faltan columnas requeridas.",
                ", ".join(sorted(missing)),
            )
        )

    if duplicated:
        errors.append(
            format_issue(
                "ERROR",
                "",
                "headers",
                "Hay columnas duplicadas.",
                ", ".join(sorted(duplicated)),
            )
        )

    if extra:
        warnings.append(
            format_issue(
                "WARNING",
                "",
                "headers",
                "Hay columnas extra. No bloquea, pero revisa si son necesarias.",
                ", ".join(sorted(extra)),
            )
        )

    return errors, warnings


def validate_row_shape(row: dict, line_num: int) -> list[str]:
    errors: list[str] = []

    if None in row:
        errors.append(
            format_issue(
                "ERROR",
                line_num,
                "row",
                "Fila mal formada. Hay columnas extra probablemente por comas sin comillas.",
                str(row[None]),
            )
        )

    return errors


def validate_required_values(row: dict[str, str], line_num: int) -> list[str]:
    errors: list[str] = []

    for column in sorted(REQUIRED_VALUE_COLUMNS):
        if not clean_text(row.get(column)):
            errors.append(
                format_issue(
                    "ERROR",
                    line_num,
                    column,
                    "Campo obligatorio vacío.",
                )
            )

    return errors


def validate_dates(row: dict[str, str], line_num: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for column in ["published_at", "collected_at"]:
        value = clean_text(row.get(column))

        if not value and column == "published_at":
            continue

        if not value and column == "collected_at":
            errors.append(
                format_issue(
                    "ERROR",
                    line_num,
                    column,
                    "Fecha de recolección obligatoria vacía.",
                )
            )
            continue

        try:
            parse_date(value)
        except ValueError as err:
            errors.append(
                format_issue(
                    "ERROR",
                    line_num,
                    column,
                    str(err),
                    value,
                )
            )

    published_at = None
    collected_at = None

    try:
        published_at = parse_date(row.get("published_at"))
    except ValueError:
        pass

    try:
        collected_at = parse_date(row.get("collected_at"))
    except ValueError:
        pass

    if published_at and collected_at and published_at > collected_at:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "published_at",
                "La fecha de publicación es posterior a collected_at. Revisa si está correcta.",
                clean_text(row.get("published_at")),
            )
        )

    return errors, warnings


def validate_salary(row: dict[str, str], line_num: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    salary_min = None
    salary_max = None

    for column in ["salary_min", "salary_max"]:
        value = clean_text(row.get(column))

        if not value:
            continue

        try:
            parsed = parse_int(value)

            if column == "salary_min":
                salary_min = parsed
            else:
                salary_max = parsed

        except ValueError as err:
            errors.append(
                format_issue(
                    "ERROR",
                    line_num,
                    column,
                    str(err),
                    value,
                )
            )

    currency = clean_text(row.get("salary_currency")).upper()

    if currency not in VALID_CURRENCIES:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "salary_currency",
                "Moneda no reconocida. Usa CLP, USD, UF o deja vacío.",
                currency,
            )
        )

    has_salary = salary_min is not None or salary_max is not None

    if has_salary and not currency:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "salary_currency",
                "Hay salario, pero falta moneda.",
            )
        )

    if salary_min is not None and salary_max is not None and salary_min > salary_max:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "salary_min/salary_max",
                "salary_min es mayor que salary_max.",
                f"{salary_min} > {salary_max}",
            )
        )

    return errors, warnings


def validate_taxonomy(row: dict[str, str], line_num: int) -> list[str]:
    warnings: list[str] = []

    modality = normalize_token(row.get("modality"))
    seniority = normalize_token(row.get("seniority"))
    category = normalize_token(row.get("category"))

    if modality and modality not in {normalize_token(item) for item in VALID_MODALITIES}:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "modality",
                "Modalidad no estándar. Sugeridas: Remoto, Hibrido, Presencial, unknown.",
                clean_text(row.get("modality")),
            )
        )

    if seniority and seniority not in {normalize_token(item) for item in VALID_SENIORITIES}:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "seniority",
                "Seniority no estándar. Sugeridos: trainee, junior, semi_senior, senior, unknown.",
                clean_text(row.get("seniority")),
            )
        )

    if category and category not in {normalize_token(item) for item in VALID_CATEGORIES}:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "category",
                "Categoría no estándar. Sugeridas: Backend, Frontend, "
                "Fullstack, Data, DevOps, QA, Support, Security, Management, "
                "Other.",
                clean_text(row.get("category")),
            )
        )

    return warnings


def validate_content(row: dict[str, str], line_num: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    title = clean_text(row.get("title"))
    description = clean_text(row.get("description"))
    source_url = clean_text(row.get("source_url"))
    technologies = split_technologies(row.get("technologies_raw"))

    if source_url and not source_url.startswith(("http://", "https://")):
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "source_url",
                "La URL no empieza con http:// o https://.",
                source_url,
            )
        )

    if title and len(title) > 260:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "title",
                "Título demasiado largo. Puede exceder el modelo de datos.",
                title[:120] + "...",
            )
        )

    if description and len(description) < 40:
        warnings.append(
            format_issue(
                "WARNING",
                line_num,
                "description",
                "Descripción muy corta. Puede afectar extracción de tecnologías.",
                description,
            )
        )

    if not technologies:
        errors.append(
            format_issue(
                "ERROR",
                line_num,
                "technologies_raw",
                "No hay tecnologías detectables.",
            )
        )

    for tech in technologies:
        if len(tech) > 180:
            warnings.append(
                format_issue(
                    "WARNING",
                    line_num,
                    "technologies_raw",
                    "Tecnología demasiado larga. El importador la puede omitir.",
                    tech[:120] + "...",
                )
            )

    return errors, warnings


def validate_duplicates(
    row: dict[str, str],
    line_num: int,
    seen_urls: dict[str, int],
    seen_title_company: dict[str, int],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    source_url = clean_text(row.get("source_url"))
    title = clean_text(row.get("title")).lower()
    company = clean_text(row.get("company")).lower()

    if source_url:
        if source_url in seen_urls:
            errors.append(
                format_issue(
                    "ERROR",
                    line_num,
                    "source_url",
                    f"URL duplicada. Ya apareció en línea {seen_urls[source_url]}.",
                    source_url,
                )
            )
        else:
            seen_urls[source_url] = line_num

    if title and company:
        key = f"{title}::{company}"

        if key in seen_title_company:
            message = (
                "Posible duplicado por título y empresa. "
                f"Ya apareció en línea {seen_title_company[key]}."
            )

            warnings.append(
                format_issue(
                    "WARNING",
                    line_num,
                    "title/company",
                    message,
                    f"{title} / {company}",
                )
            )
        else:
            seen_title_company[key] = line_num

    return errors, warnings


def validate_csv(file_path: Path, strict: bool = False) -> int:
    if not file_path.exists():
        print(f"ERROR: No existe el archivo: {file_path}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    seen_urls: dict[str, int] = {}
    seen_title_company: dict[str, int] = {}

    total_rows = 0

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        header_errors, header_warnings = validate_headers(reader.fieldnames)
        errors.extend(header_errors)
        warnings.extend(header_warnings)

        if header_errors:
            print_report(file_path, total_rows, errors, warnings)
            return 1

        for row in reader:
            total_rows += 1
            line_num = reader.line_num

            shape_errors = validate_row_shape(row, line_num)
            errors.extend(shape_errors)

            if shape_errors:
                continue

            row_errors = []
            row_warnings = []

            row_errors.extend(validate_required_values(row, line_num))

            date_errors, date_warnings = validate_dates(row, line_num)
            row_errors.extend(date_errors)
            row_warnings.extend(date_warnings)

            salary_errors, salary_warnings = validate_salary(row, line_num)
            row_errors.extend(salary_errors)
            row_warnings.extend(salary_warnings)

            content_errors, content_warnings = validate_content(row, line_num)
            row_errors.extend(content_errors)
            row_warnings.extend(content_warnings)

            duplicate_errors, duplicate_warnings = validate_duplicates(
                row,
                line_num,
                seen_urls,
                seen_title_company,
            )
            row_errors.extend(duplicate_errors)
            row_warnings.extend(duplicate_warnings)

            row_warnings.extend(validate_taxonomy(row, line_num))

            errors.extend(row_errors)
            warnings.extend(row_warnings)

    print_report(file_path, total_rows, errors, warnings)

    if errors:
        return 1

    if strict and warnings:
        return 1

    return 0


def print_report(file_path: Path, total_rows: int, errors: list[str], warnings: list[str]) -> None:
    print()
    print("VALIDACIÓN CSV")
    print(f"Archivo: {file_path}")
    print(f"Filas leídas: {total_rows}")
    print(f"Errores: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print()

    if errors:
        print("ERRORES:")
        for issue in errors:
            print(issue)
        print()

    if warnings:
        print("WARNINGS:")
        for issue in warnings:
            print(issue)
        print()

    if not errors:
        print("CSV válido para importar.")

        if warnings:
            print("Hay warnings, pero no bloquean la importación.")
    else:
        print("CSV con errores. Corrige antes de importar.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validar CSV de ofertas laborales.")
    parser.add_argument("file", type=Path, help="Ruta al archivo CSV.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Hace que los warnings también fallen.",
    )

    args = parser.parse_args()
    exit_code = validate_csv(args.file, strict=args.strict)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
