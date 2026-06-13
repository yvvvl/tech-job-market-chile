import type { ReactNode } from "react";

export function Section({
  title,
  description,
  action,
  children,
  className = "",
}: {
  title: string;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={`rounded-2xl border border-border/60 bg-card/50 p-6 shadow-card ${className}`}>
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          <h3 className="text-base font-semibold tracking-tight">{title}</h3>
          {description ? (
            <p className="mt-1 text-sm text-muted-foreground">{description}</p>
          ) : null}
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}

export function PageHeader({
  eyebrow,
  title,
  description,
  children,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  children?: ReactNode;
}) {
  return (
    <div className="mb-10 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div className="max-w-2xl animate-fade-up">
        {eyebrow ? (
          <p className="mb-2 text-xs uppercase tracking-[0.2em] text-primary">{eyebrow}</p>
        ) : null}
        <h1 className="font-display text-3xl sm:text-4xl font-semibold tracking-tight text-gradient">
          {title}
        </h1>
        {description ? (
          <p className="mt-3 text-sm sm:text-base text-muted-foreground">{description}</p>
        ) : null}
      </div>
      {children}
    </div>
  );
}
