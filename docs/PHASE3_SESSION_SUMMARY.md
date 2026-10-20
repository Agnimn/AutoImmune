# AutoImmune: Session Activity & Progress Summary

**Date:** 2026-10-20  
**Repository:** `AutoImmune` (Java Spring Boot self-healing pipeline research prototype)  
**Task Focus:** Phase 3 Pre-Flight Reconciliation, LLM Provider Integration, Sampling/Disagreement (Hypothesis H1), Evidence Schema Extension, and Analysis Separation.

---

## 1. What You Asked

### Initial Request: Mandatory Pre-Flight Reconciliation for Phase 3
1. **Reconcile repository with Master Plan:**
   - Read `AGENTS.md`, `docs/PLAN.md`, `docs/TEAM_WORKFLOW.md`, `README.md`, and the current codebase.
   - Treat the repository as the source of truth for what was implemented, and the master plan as the source of truth for intended behaviour.
   - Produce a concise mapping:
     - Implemented and tested.
     - Implemented but not verified.
     - Missing requirements.
     - Conflicts between repo, master plan, and requirements.
   - Do not rebuild working components; preserve existing interfaces and tests.
   - Prioritise missing provider-layer requirements, multi-sample diagnosis for Hypothesis H1, schema fields, secret-scan test, and analysis separation.

### Subsequent Prompts:
2. **"continue"**:
   - Approved the step-by-step pre-flight reconciliation plan to implement Step A through Step J.
3. **"pls finish fast i need to go to pahse 4"**:
   - Fast-track all remaining Phase 3 implementation tasks and tests so the project is immediately ready for Phase 4.
4. **"just give me detailed md file of what i asekd u and what u did until now"**:
   - Generate this complete and detailed summary markdown file.

---

## 2. What Was Accomplished (Step-by-Step Breakdown)

### Step 0: Pre-Flight Audit & Baseline Verification
- Audited all existing modules: `providers.py`, `decide.py`, `record.py`, `orchestrator.py`, `detector.py`, `sandbox.py`, `deploy.py`, `analyse.py`.
- Formulated `docs/phase3_reconciliation.md` mapping all existing features, gaps, and canonical field names.
- Verified test baseline using the repository's `.venv` environment (149 passing tests).

---

### Step A: Correct Layout Line in `AGENTS.md`
- **File modified:** [AGENTS.md](AGENTS.md)
- Fixed the layout line from referencing a non-existent `F05` (`faults/F01, F04, F05, F06/` → `faults/F01, F04, F06/`).

---

### Step B: Hypothesis H1 Multi-Sample Diagnosis & Disagreement Escalation
- **Files modified:** [pipeline/providers.py](pipeline/providers.py), [config/decision.yaml](config/decision.yaml), [pipeline/__main__.py](pipeline/__main__.py)
- **Data model update:**
  - Added `samples: list[dict] = field(default_factory=list)` and `samples_disagree: bool | None = None` to the `Diagnosis` dataclass.
- **Provider sampling logic:**
  - Extended `LLMProvider.diagnose()` to accept `n_samples` and `sample_temperature`.
  - When `n_samples > 1`, queries the LLM repeatedly with independent cache keys (material includes sample index).
  - Evaluates disagreement: flags `samples_disagree = True` if the rank-1 suspect file differs across samples.
- **Decision engine integration:**
  - `decide.py` checks `diagnosis.samples_disagree`; if `True`, candidate is escalated (`ESCALATE`, tier `medium`, reason `diagnosis_samples_disagree`).
- **Configuration & CLI:**
  - Added `diag_samples: 1` and `diag_temperature: 0.7` to `config/decision.yaml`.
  - Added `--diag-samples` CLI argument to `pipeline/__main__.py`.

---

### Step C: Top-1 and Top-3 Localisation Accuracy Tracking
- **File modified:** [pipeline/orchestrator.py](pipeline/orchestrator.py)
- In Step 4 of the orchestrator run:
  - Added `_hit_flags(diagnosis, fault, repo_dir)` comparing diagnosis causes against `fault.json[diagnosed_file]`.
  - Computes `top1_hit` and `top3_hit` booleans (forced to `None` for oracle localisation).
  - Persisted in `runs/<run_id>/diagnosis.json` and passed to `build_row()`.
  - Evaluator-side only: never exposed to LLM prompts or `decide.py`.

---

### Step D: Evidence Schema Extension (`record.py`)
- **Files modified:** [pipeline/record.py](pipeline/record.py), [tests/test_record.py](tests/test_record.py)
- Preserved `additionalProperties: false` integrity while adding 7 nullable fields to `EVIDENCE_SCHEMA` and `build_row()`:
  1. `diag_samples`: `integer | null`
  2. `samples_disagree`: `boolean | null`
  3. `top1_hit`: `boolean | null`
  4. `top3_hit`: `boolean | null`
  5. `model`: `string | null`
  6. `llm_attempts`: `integer | null`
  7. `apply_error`: `string | null`
- Updated fixture helper `_row()` in `tests/test_record.py` so all existing and new schema tests pass.

---

### Step E: Replay Cache Tracking & Secret Sanitation
- **Files modified:** [.gitignore](.gitignore), [tests/test_providers.py](tests/test_providers.py)
- **`.gitignore` update:**
  - Allowed `cache/*.json` to be committed and tracked in git while keeping other temporary directories ignored:
    ```gitignore
    cache/*
    !cache/.gitkeep
    !cache/*.json
    ```
- **Secret scan test:**
  - Added `test_cache_files_contain_no_secrets` in `tests/test_providers.py` to ensure no `Bearer `, `sk-`, `api_key`, or raw credentials can be saved into cache files.

---

### Step F: LLM Smoke Test Tool
- **File created:** [tools/llm_smoke.py](tools/llm_smoke.py)
- Standalone CLI tool to test live LLM connectivity, authentication, and diagnosis specifically on fault `F06` without triggering full pipeline runs.
- Includes support for `--mode live|replay` and `--samples N`.

---

### Step G & H: Gate-Only Mode & Orchestrator Safety
- **Files modified:** [pipeline/__main__.py](pipeline/__main__.py), [pipeline/orchestrator.py](pipeline/orchestrator.py)
- Added `--gates-only` flag to allow running validation gates V0–V3 and computing decisions without triggering deployment or rollbacks during live testing.

---

### Step I: Analysis Metric Separation & Localisation Reporting
- **Files modified:** [analyse.py](analyse.py), [tests/test_analyse.py](tests/test_analyse.py)
- **Separation:**
  - Scripted benchmark rows and LLM rows (where `diag_mode` or `patch_mode` is `live` or `replay`) are strictly partitioned.
  - Scripted rows are never attributed to LLM execution.
- **Accuracy Metrics:**
  - Calculates top-1 and top-3 localisation accuracy with Wilson 95% confidence intervals per fault and per model.
  - Generates `llm_units.csv` and `llm_diagnosis.csv` when LLM candidate rows are detected.
- **Unit test:** Added `test_llm_and_scripted_rows_are_reported_in_separate_tables`.

---

### Step J: Documentation
- **File created:** [docs/PHASE3_NOTES.md](docs/PHASE3_NOTES.md)
  - Documents the bounded LLM architecture, Hypothesis H1 sampling, schema definitions, replay cache rules, and analysis methodology.

---

## 3. Verification & Current Test Status

Running the complete non-docker test suite:
```powershell
.venv\Scripts\python.exe -m pytest -m "not docker"
```
**Result:**
```
===================== 154 passed, 16 deselected in 7.53s =====================
```
All 154 tests pass cleanly with 0 failures, 0 errors, and no regressions across existing modules.

Running `analyse.py`:
```powershell
.venv\Scripts\python.exe analyse.py
```
**Result:**
Generates pilot report and CSV tables deterministically with zero errors.

---

## 4. Phase 4 Readiness

The repository is now fully prepared for **Phase 4 (Live Experiments, Replay Artifacts & Empirical Evaluation)**:
- Live LLM calls can be executed via `python -m pipeline run --fault F06 --diag-mode live --patch-mode live --gates-only`.
- Cached responses will be stored in `cache/*.json` and tracked in git.
- Offline evaluation can be run deterministically with `--diag-mode replay --patch-mode replay`.
- `analyse.py` will automatically produce separate tables for LLM vs. scripted performance.
