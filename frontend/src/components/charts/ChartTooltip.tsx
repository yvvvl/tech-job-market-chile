export function DarkTooltip(props: any) {
  const { active, payload, label } = props ?? {};
  if (!active || !payload || payload.length === 0) return null;
  return (
    <div className="rounded-lg border border-border/80 bg-popover/95 px-3 py-2 text-xs shadow-glow backdrop-blur">
      {label ? <p className="mb-1 font-medium text-foreground">{label}</p> : null}
      <div className="space-y-0.5">
        {payload.map((p: any, i: number) => (
          <div key={i} className="flex items-center gap-2 text-muted-foreground">
            <span
              className="h-2 w-2 rounded-full"
              style={{ backgroundColor: p.color ?? p.fill ?? "var(--color-primary)" }}
            />
            <span>{p.name}</span>
            <span className="ml-auto font-mono text-foreground">
              {typeof p.value === "number" ? p.value.toLocaleString() : p.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
