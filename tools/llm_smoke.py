"""Single-call smoke test for LLM diagnosis on fault F06.

Usage:
    python tools/llm_smoke.py [--mode live|replay] [--samples N]

Requires:
    LLM_BASE_URL, LLM_MODEL, and LLM_API_KEY environment variables (in live mode).
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from pipeline.providers import get_provider, ProviderError


def load_order_sources() -> dict[str, str]:
    src_dir = REPO / "app" / "src" / "main" / "java" / "com" / "autoimmune" / "orders"
    sources = {}
    for p in sorted(src_dir.glob("*.java")):
        rel = p.relative_to(REPO).as_posix()
        sources[rel] = p.read_text(encoding="utf-8")
    return sources


def f06_incident() -> dict:
    return {
        "run_id": "smoke-f06",
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fault_id": "F06",
        "rule": "probe_mismatch",
        "rules_fired": ["probe_mismatch"],
        "kind": "probe_mismatch",
        "endpoint": "/api/orders/2/discount",
        "status": 200,
        "expected": 900.00,
        "actual": 1000.00,
        "stack_trace": None,
        "evidence": "GET /api/orders/2/discount returned 1000.00 instead of expected 900.00 (discount not applied at threshold).",
    }


def main():
    parser = argparse.ArgumentParser(description="LLM diagnosis smoke test on F06")
    parser.add_argument("--mode", choices=["live", "replay"], default="live",
                        help="Provider mode (default: live)")
    parser.add_argument("--samples", type=int, default=1,
                        help="Number of diagnosis samples (default: 1)")
    args = parser.parse_args()

    print(f"=== AutoImmune LLM Smoke Test (F06) [mode={args.mode}, samples={args.samples}] ===")
    if args.mode == "live":
        missing = [k for k in ("LLM_BASE_URL", "LLM_MODEL") if not os.environ.get(k)]
        if missing:
            print(f"ERROR: Missing environment variables for live mode: {', '.join(missing)}", file=sys.stderr)
            print("Set them before running: export LLM_BASE_URL=... LLM_MODEL=...", file=sys.stderr)
            sys.exit(1)
        print(f"Base URL: {os.environ.get('LLM_BASE_URL')}")
        print(f"Model:    {os.environ.get('LLM_MODEL')}")

    sources = load_order_sources()
    print(f"Loaded {len(sources)} source files from app/src/main/java/com/autoimmune/orders")

    incident = f06_incident()
    print(f"Incident: {incident['endpoint']} -> expected={incident['expected']}, actual={incident['actual']}")

    try:
        kwargs = {}
        if args.mode in ("live", "replay"):
            kwargs["n_samples"] = args.samples
        provider = get_provider(args.mode, **kwargs)
        print(f"Calling provider.diagnose()...")
        diag = provider.diagnose(incident, sources)
    except ProviderError as err:
        print(f"FAILED: ProviderError: {err}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"FAILED: Unexpected error: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(3)

    print("\n--- Diagnosis Result ---")
    print(f"Provider mode:    {diag.provider_mode}")
    print(f"Model:            {diag.model}")
    print(f"Oracle fallback:  {diag.oracle_localisation}")
    print(f"Disagreement:     {diag.samples_disagree}")
    print(f"Attempts:         {len(diag.attempts)}")
    print("Causes:")
    for c in diag.causes:
        print(f"  [Rank {c.rank}] {c.file}:{c.line}")
        print(f"     Reason:   {c.reason}")
        print(f"     Evidence: {c.evidence}")

    f06_target = "app/src/main/java/com/autoimmune/orders/OrderService.java"
    top1 = diag.causes[0].file == f06_target if diag.causes else False
    top3 = any(c.file == f06_target for c in diag.causes[:3])
    print(f"\nTop-1 hit on OrderService.java: {top1}")
    print(f"Top-3 hit on OrderService.java: {top3}")
    print("\nSmoke test completed successfully.")


if __name__ == "__main__":
    main()
