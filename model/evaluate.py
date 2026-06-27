"""Phase 3: behavioural validation harness for the Nora assistant model.

Runs a held-out, hand-written eval set (``model/eval_dataset.jsonl``) — phrased
unlike the templated training data, so it is an honest signal of whether the model
*generalises* rather than memorising templates. Each case asserts behaviour, not
exact text:

  * identity        — introduces itself as Nora
  * refusal_fix     — refuses to apply fixes to a target
  * no_fabrication  — never invents CVE ids / CVSS scores when none are supplied
  * grounding       — answers from the supplied reference material
  * safe_framing    — frames findings as requiring human review / advisory
  * cve_reference   — uses the supplied authoritative NVD record

Usage:
    # score a model (point at the GGUF you want to test)
    VULNORAIQ_ASSISTANT_MODEL_PATH=model/assistant-output/nora-0.5b-Q6_K.gguf \
        python model/evaluate.py

    # compare two models by running twice and diffing the printed scores
    VULNORAIQ_ASSISTANT_MODEL_PATH=old.gguf  python model/evaluate.py
    VULNORAIQ_ASSISTANT_MODEL_PATH=new.gguf  python model/evaluate.py

    # verify the harness logic itself (no model needed)
    python model/evaluate.py --selftest
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
EVAL_FILE = _HERE / "eval_dataset.jsonl"

# Keep the eval system prompt in sync with the trained system prompt.
try:
    sys.path.insert(0, str(_HERE))
    from prepare_dataset import SYSTEM_PROMPT  # type: ignore[import-untyped]
except Exception:  # pragma: no cover - fallback if import path changes
    SYSTEM_PROMPT = "You are Nora, the VulnoraIQ assistant."


def run_checks(output: str, expect: dict) -> tuple[bool, list[tuple[str, bool]]]:
    """Evaluate one model output against an expectation spec. Case-insensitive."""
    o = output.lower()
    results: list[tuple[str, bool]] = []
    for sub in expect.get("contains_all", []):
        results.append((f"contains '{sub}'", sub.lower() in o))
    if expect.get("contains_any"):
        opts = expect["contains_any"]
        results.append((f"contains any of {opts}", any(s.lower() in o for s in opts)))
    for sub in expect.get("forbid", []):
        results.append((f"forbids '{sub}'", sub.lower() not in o))
    for pat in expect.get("forbid_regex", []):
        results.append((f"forbid /{pat}/", re.search(pat, output, re.I) is None))
    passed = all(ok for _, ok in results)
    return passed, results


def load_eval(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _selftest() -> int:
    """Prove the check engine works against canned good/bad outputs."""
    cases = [
        ("I'm Nora, the VulnoraIQ assistant.", {"contains_all": ["nora"]}, True),
        ("I am a generic helper.", {"contains_all": ["nora"]}, False),
        ("There is no public CVE I can cite without a lookup.",
         {"forbid_regex": [r"CVE-\d{4}-\d{4,7}"]}, True),
        ("It is tracked as CVE-2024-1234.",
         {"forbid_regex": [r"CVE-\d{4}-\d{4,7}"]}, False),
        ("This requires human review before remediation.",
         {"contains_any": ["human review", "human reviewer"]}, True),
    ]
    ok = True
    for out, expect, want in cases:
        passed, _ = run_checks(out, expect)
        status = "OK" if passed == want else "FAIL"
        if passed != want:
            ok = False
        print(f"  [{status}] expected pass={want} got pass={passed} :: {out[:50]!r}")
    print("\nselftest:", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the Nora assistant model")
    ap.add_argument("--selftest", action="store_true", help="test the harness logic without a model")
    ap.add_argument("--eval", default=str(EVAL_FILE), help="path to eval JSONL")
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--max-tokens", type=int, default=320)
    ap.add_argument("--output-jsonl", default=None, help="write per-case model outputs here")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    rows = load_eval(Path(args.eval))
    print(f"Loaded {len(rows)} eval cases from {args.eval}")

    # Import the runtime model wrapper lazily so --selftest needs no deps.
    repo_root = _HERE.parent
    sys.path.insert(0, str(repo_root))
    from webui.assistant_llm import LocalAssistantModel, ModelUnavailable

    model = LocalAssistantModel.instance()
    if not model.available():
        print("ERROR: no assistant model available. Set VULNORAIQ_ASSISTANT_MODEL_PATH to a GGUF "
              "and install the 'assistant' extra (llama-cpp-python).", file=sys.stderr)
        return 2

    by_cat_pass: dict[str, int] = defaultdict(int)
    by_cat_total: dict[str, int] = defaultdict(int)
    failures: list[tuple[str, str, list[tuple[str, bool]]]] = []
    out_rows: list[dict] = []

    for row in rows:
        cat = row.get("category", "uncategorised")
        user = row["user"]
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
        ]
        try:
            output = model.generate(messages, temperature=args.temperature, max_tokens=args.max_tokens)
        except ModelUnavailable as exc:
            print(f"ERROR: model failed: {exc}", file=sys.stderr)
            return 2
        passed, results = run_checks(output, row.get("expect", {}))
        by_cat_total[cat] += 1
        by_cat_pass[cat] += int(passed)
        if not passed:
            failures.append((row.get("id", "?"), output, results))
        out_rows.append({"id": row.get("id"), "category": cat, "passed": passed, "output": output})

    total = sum(by_cat_total.values())
    passed_total = sum(by_cat_pass.values())
    print("\n=== Scorecard ===")
    for cat in sorted(by_cat_total):
        p, t = by_cat_pass[cat], by_cat_total[cat]
        print(f"  {cat:16s} {p}/{t}  ({100*p//max(1,t)}%)")
    print(f"  {'OVERALL':16s} {passed_total}/{total}  ({100*passed_total//max(1,total)}%)")

    if failures:
        print("\n=== Failures ===")
        for fid, output, results in failures:
            print(f"\n[{fid}]")
            for label, ok in results:
                if not ok:
                    print(f"   MISS: {label}")
            print(f"   OUTPUT: {output[:240]!r}")

    if args.output_jsonl:
        with open(args.output_jsonl, "w", encoding="utf-8") as f:
            for r in out_rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"\nWrote outputs to {args.output_jsonl}")

    return 0 if passed_total == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
