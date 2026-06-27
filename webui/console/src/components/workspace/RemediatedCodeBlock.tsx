import { useState } from "react";
import { Check, ClipboardCopy, ShieldCheck, Sparkles } from "lucide-react";
import type { Remediation } from "@/types";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast";
import { cn } from "@/lib/utils";
import { CodeLines } from "./CodeLines";

interface RemediatedCodeBlockProps {
  remediation: Remediation;
  onMarkForReview: () => void;
}

export function RemediatedCodeBlock({
  remediation,
  onMarkForReview,
}: RemediatedCodeBlockProps) {
  const { notify } = useToast();
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(remediation.secureCode.code);
      setCopied(true);
      notify("Mitigation guidance copied to clipboard");
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      notify("Copy failed — select the guidance manually", "info");
    }
  };

  const confidenceTone =
    remediation.confidence >= 85
      ? "text-severity-low"
      : remediation.confidence >= 65
        ? "text-severity-medium"
        : "text-severity-high";

  return (
    <section className="overflow-hidden rounded-lg border border-[var(--accent-sage)]/45 bg-card shadow-card">
      <header className="flex flex-wrap items-center gap-2 border-b border-border bg-[color-mix(in_srgb,var(--accent-sage)_10%,transparent)] px-3 py-2">
        <ShieldCheck className="size-4 text-[var(--accent-sage)]" />
        <span className="text-xs font-bold uppercase tracking-wide text-[var(--accent-sage)]">
          Recommended Mitigation
        </span>
        {remediation.secureCode.language && (
          <span className="rounded border border-border bg-card px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
            {remediation.secureCode.language}
          </span>
        )}
        <span
          className={cn("ml-auto inline-flex items-center gap-1 text-[11px] font-bold", confidenceTone)}
          title="Mitigation confidence"
        >
          <Sparkles className="size-3" />
          {remediation.confidence}% confidence
        </span>
      </header>

      <div className="space-y-3 p-3">
        <CodeLines block={remediation.secureCode} accent="success" />

        <div className="flex flex-wrap gap-2">
          <Button variant="success" size="sm" onClick={handleCopy}>
            {copied ? <Check className="size-4" /> : <ClipboardCopy className="size-4" />}
            {copied ? "Copied" : "Copy Mitigation"}
          </Button>
          <Button variant="outline" size="sm" onClick={onMarkForReview}>
            Mark for Review
          </Button>
        </div>

        <div className="rounded-md border border-border bg-muted p-3">
          <p className="text-xs font-bold text-foreground">Why this mitigation helps</p>
          <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
            {remediation.rationale}
          </p>
          <p className="mt-2 text-[11px] italic text-muted-foreground">
            VulnoraIQ provides mitigation guidance only; it does not apply changes to the target. A human owner must implement and verify any change.
          </p>
        </div>
      </div>
    </section>
  );
}
