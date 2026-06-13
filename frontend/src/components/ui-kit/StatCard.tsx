import { ArrowDownRight, ArrowUpRight, type LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { useT } from "@/lib/i18n";

export function StatCard({
  label,
  value,
  delta,
  icon: Icon,
  hint,
}: {
  label: string;
  value: string | number;
  delta?: number;
  icon: LucideIcon;
  hint?: string;
}) {
  const t = useT();
  const positive = (delta ?? 0) >= 0;
  return (
    <div className="group relative overflow-hidden rounded-2xl border border-border/60 bg-card/60 p-5 shadow-card transition hover:border-primary/40">
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition pointer-events-none bg-hero" />
      <div className="relative flex items-start justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.14em] text-muted-foreground">{label}</p>
          <p className="mt-3 font-display text-3xl font-semibold tracking-tight">{value}</p>
          {hint ? <p className="mt-1 text-xs text-muted-foreground">{hint}</p> : null}
        </div>
        <div className="grid h-10 w-10 place-items-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20">
          <Icon className="h-4 w-4" />
        </div>
      </div>
      {typeof delta === "number" ? (
        <div
          className={cn(
            "relative mt-4 inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs",
            positive
              ? "border-[color:var(--color-success)]/30 text-[color:var(--color-success)] bg-[color:var(--color-success)]/10"
              : "border-destructive/30 text-destructive bg-destructive/10",
          )}
        >
          {positive ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
          {Math.abs(delta)}% {t("stat.vsLastMonth")}
        </div>
      ) : null}
    </div>
  );
}
