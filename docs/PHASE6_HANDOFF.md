# AutoImmune — Phase 6 Handoff

For the teammate responsible for live LLM integration.  
This document contains no secrets, no hidden-test content, and no fabricated results.

---

## What Phase 5 left for Phase 6

Phase 5 proved the scripted and rule-mode pipeline end-to-end (170 tests passing, 16 scripted candidates
validated across F01/F04/F06). The following items remain and require a live or replay LLM provider:

1. Configure the hosted or local endpoint in `.env`
2. Run `tools/llm_smoke.py` to verify the connection
3. Run live diagnosis (3 samples per fault) and patch drafting for F06, F01, F04 with `--gates-only`
4. Record `cache/` entries from the live run
5. Replay them with no network (`--diag-mode replay --patch-mode replay`) and verify identical results
6. Run `analyse.py` and read the separate LLM tables in `results/llm_units.csv` and `results/llm_diagnosis.csv`
7. Fill the real numbers (calls, invalid responses, retries, patches that did not apply) in Phase 6 notes

---

## Acceptance checks that remain open

| Check | What is needed |
|-------|---------------|
| A3 (diagnosis) | Live run produces `diagnosis.json` with ≤3 ranked causes; `provider_mode=live`; `top1_hit` and `top3_hit` logged |
| A4 (candidates) | Live run produces 3 candidate diffs; each applies cleanly or is rejected with `apply_error` logged |
| Replay equals live | Replay run with same cache entry produces identical gate results and decision |
| H1 data | `samples_disagree`, `top1_hit`, `top3_hit` populated for each fault from at least 1 live run per fault |

---

## Step-by-step instructions

### 1. Install Ollama and pull the model

1. Download and install Ollama from [https://ollama.com](https://ollama.com).
2. Pull the target model in your terminal:
   ```powershell
   ollama pull qwen2.5-coder:7b
   ```
3. Ensure Ollama is running (`curl http://localhost:11434/api/tags` or check the taskbar icon).

### 2. Configure environment variables in your terminal

Python reads directly from your shell environment (it does not auto-load `.env`). Set the variables in your active terminal:

**In PowerShell:**
```powershell
$env:LLM_BASE_URL = "http://localhost:11434/v1"
$env:LLM_MODEL    = "qwen2.5-coder:7b"
$env:LLM_API_KEY  = ""  # optional for local Ollama
```

*(In Linux / macOS bash, use `export LLM_BASE_URL="http://localhost:11434/v1"`, `export LLM_MODEL="qwen2.5-coder:7b"`, `export LLM_API_KEY=""`)*

### 3. Verify the connection via smoke test

```powershell
.venv\Scripts\python.exe tools\llm_smoke.py
```

Expected output: a short diagnosis JSON and a diff snippet. If it fails, check the URL, model name, and key.

### 3. Run live diagnosis + scripted gates (gates-only)

```powershell
# Run 3 diagnosis samples per fault; stop after gates (do not deploy)
.venv\Scripts\python.exe -m pipeline run --fault F06 --diag-mode live --patch-mode scripted `
    --diag-samples 3 --gates-only

.venv\Scripts\python.exe -m pipeline run --fault F01 --diag-mode live --patch-mode scripted `
    --diag-samples 3 --gates-only

.venv\Scripts\python.exe -m pipeline run --fault F04 --diag-mode live --patch-mode scripted `
    --diag-samples 3 --gates-only
```

Each run writes cache entries to `cache/` and evidence rows to `results/evidence.jsonl`.

### 4. Run live patch drafting (if model can produce valid diffs)

```powershell
.venv\Scripts\python.exe -m pipeline run --fault F06 --diag-mode live --patch-mode live --gates-only
```

Note: small models often produce diffs that do not apply (`apply_error` will be set). This is a valid
research outcome — record it honestly.

### 5. Replay run (no network)

After the live run has written cache entries, disconnect from the network and run:

```powershell
.venv\Scripts\python.exe -m pipeline run --fault F06 --diag-mode replay --patch-mode scripted `
    --diag-samples 3 --gates-only
```

The replay run must produce the same diagnosis as the live run (same `causes[0].file`). If not, record
the discrepancy.

### 6. Regenerate the analysis

```powershell
.venv\Scripts\python.exe analyse.py
```

Check `results/llm_units.csv` and `results/llm_diagnosis.csv` for the live/replay rows.
The pilot report will include section "e) LLM candidates and diagnosis" with `top1_hit`/`top3_hit` rates.

### 7. What a good result looks like

| Check | Good outcome |
|-------|-------------|
| `llm_smoke.py` | Exits 0, prints a valid diagnosis JSON |
| Live run | `oracle_localisation=False`, `top1_hit` and `top3_hit` logged (not null) |
| 3 samples | `samples_disagree` is True or False (not null) |
| Replay | Produces the same `causes[0].file` as the live run |
| Patch diffs | At least 1 of 3 live patches applies cleanly (`apply_error=null`) |
| V0–V3 | Gates run inside Docker; at least 1 patch reaches AUTO_APPLY |

---

## Known risks

| Risk | Mitigation |
|------|-----------|
| Free-tier rate limits change | Check the provider console before the run; use `--gates-only` to minimise calls |
| Small model produces non-applying diffs | Record `apply_error`; this is a valid result — do not hide it |
| Rule-mode oracle localisation for F04 and F06 | `oracle_localisation=True` means the rule provider read `fault.json` directly — not a measured hit rate; exclude from top1_hit/top3_hit analysis |
| Cache key collision | Cache keys are sha256 of (provider, model, prompt, temperature); changing the model or prompt invalidates existing entries |
| `samples_disagree` null with 1 sample | Use `--diag-samples 3` to enable the agreement check |

---

## Files Phase 6 may write (no approval needed from Phase 5 rules)

- `cache/*.json` — live-run cache entries
- `runs/<run_id>/` — live-run artifacts
- `results/evidence.jsonl` — append only; never hand-edit
- `results/*.csv`, `results/pilot_report.md` — regenerated by `analyse.py`
- `docs/PHASE6_NOTES.md` — your Phase 6 notes

---

## Files Phase 6 must NOT touch

- `faults/*/hidden_tests/` — never read, mount, or print
- `faults/*/candidates/labels.json` — do not alter existing labels; add `label_source` if desired but note it in your notes
- `config/decision.yaml` — do not change thresholds without team discussion
- Any existing `runs/` or `results/` entries — append only

---

## Exact commands (copied from real CLI help)

```
python -m pipeline run --help

usage: python -m pipeline run [-h] --fault FAULT --diag-mode {rule,replay,live}
                               --patch-mode {scripted,replay,live}
                               [--candidate CANDIDATE] [--deploy-each]
                               [--run-id RUN_ID] [--diag-samples DIAG_SAMPLES]
                               [--gates-only]
```

---

## Contact and review

All labels are currently "draft: team to review". Before publishing any H1 results or LLM accuracy claims,
do a two-person review of `faults/*/candidates/labels.json` (Agni M N, Pradeep S, S Nehal, Mrs. M. Shona).
