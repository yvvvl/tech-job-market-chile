type TooltipPayloadItem = {
  name?: string | number;
  value?: string | number;
};

type DarkTooltipProps = {
  active?: boolean;
  label?: string | number;
  payload?: TooltipPayloadItem[];
};

export function DarkTooltip({ active, payload, label }: DarkTooltipProps) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  return (
    <div className="rounded-lg border border-border bg-card/95 px-3 py-2 text-xs shadow-lg backdrop-blur">
      {label ? (
        <p className="mb-1 font-medium text-foreground">{label}</p>
      ) : null}

      <div className="space-y-1">
        {payload.map((item, index) => (
          <div
            key={`${item.name ?? "item"}-${index}`}
            className="flex items-center justify-between gap-4"
          >
            <span className="text-muted-foreground">{item.name}</span>
            <span className="font-mono text-foreground">
              {typeof item.value === "number"
                ? item.value.toLocaleString()
                : item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
