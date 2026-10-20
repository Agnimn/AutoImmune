# AutoImmune Phase 3 Notes: LLM Provider Integration & Evidence Architecture

This document records the architectural details, schema extensions, sampling mechanisms, cache policies, and validation gates implemented during Phase 3 of the AutoImmune project.

---

## 1. LLM Boundary and Provider Integration

In AutoImmune, LLMs are strictly bounded:
- **Scope**: Used **only** for `diagnose()` (fault localisation from incident + sources) and `draft_patches()` (generating candidate diffs).
- **Control**: Deterministic pipeline with fixed control flow (no autonomous agent loops, no tool calling).
- **Retry Policy**: Bounded to 3 attempts with clear JSON-repair feedback if validation against `DIAGNOSIS_SCHEMA` or `PATCHES_SCHEMA` fails.
- **Provider Modes**:
  1. `rule`: Deterministic stack-trace frame extraction and heuristic fallback.
  2. `scripted`: Deterministic benchmark patches (`candidates/*.diff`).
  3. `replay`: Offline cached responses indexed by SHA-256 of canonical prompt payloads without network access.
  4. `live`: OpenAI-compatible endpoint calls over HTTP with exponential/retry handling.

Every artifact, decision, and evidence row logs `diag_mode` and `patch_mode` separately. Scripted and rule results are never attributed to LLM execution.

---

## 2. Hypothesis H1: Multi-Sample Diagnosis & Disagreement Escalation

Phase 3 operationalises Hypothesis H1:
> *"Does sampling diagnosis hypotheses multiple times catch hallucinations and prevent risky auto-applications?"*

- **Sampling Configuration**:
  - `config/decision.yaml`: Configured via `diag_samples` (default: 1) and `diag_temperature` (default: 0.7).
  - CLI override: `--diag-samples N`.
- **Disagreement Detection**:
  - When `diag_samples > 1`, `LLMProvider.diagnose()` executes `N` independent samples (each with a distinct cache key including sample index).
  - If the rank-1 suspect file differs across samples, `Diagnosis.samples_disagree` is flagged `True`.
- **Decision Engine Integration**:
  - `decide.py` inspects `diagnosis.samples_disagree`.
  - When `True`, the candidate is escalated to human review (`ESCALATE`, tier `medium`, reason `diagnosis_samples_disagree`), overriding what would otherwise be `AUTO_APPLY`.

---

## 3. Evidence Schema Extensions

To support Phase 3 empirical evaluation, `EVIDENCE_SCHEMA` in `pipeline/record.py` was extended with 7 nullable fields (`additionalProperties: false` preserved):

| Field | Type | Description |
|---|---|---|
| `diag_samples` | `integer \| null` | Number of diagnosis samples requested. |
| `samples_disagree` | `boolean \| null` | `True` if rank-1 files differed across samples; `None` if single-sample or rule mode. |
| `top1_hit` | `boolean \| null` | `True` if rank-1 suspected file matched `fault.json[diagnosed_file]`. `None` for oracle localisation. |
| `top3_hit` | `boolean \| null` | `True` if any top-3 suspected file matched `fault.json[diagnosed_file]`. |
| `model` | `string \| null` | LLM model identifier (null for rule/scripted). |
| `llm_attempts` | `integer \| null` | Number of attempts required to obtain a valid JSON response. |
| `apply_error` | `string \| null` | Git apply error message if candidate patch failed syntactic application. |

All new fields default to `null` to ensure full backward compatibility with pre-Phase-3 scripted benchmark rows.

---

## 4. Replay Cache & Secret Sanitation

- **Tracking**: `cache/*.json` is tracked in version control, allowing deterministic replay runs across machines without network access or API key disclosure.
- **Key Material**: Cache keys are SHA-256 hashes of canonicalised message payloads + temperature + sample index. `fault_id` is excluded from cache keys to prevent data leakage.
- **Secret Scanning**: Pytest automated checks (`test_cache_files_contain_no_secrets`) scan all `cache/*.json` entries to verify no `Bearer `, `sk-`, `api_key`, or raw credentials can ever be saved into the replay cache.

---

## 5. Analysis & Metric Reporting

`analyse.py` has been updated to strictly partition benchmark results:
- **Separation**: Scripted candidate baselines and LLM-generated candidates are processed into independent tables.
- **Localisation Accuracy**: Computes top-1 and top-3 diagnosis hit rates per fault and per model along with Wilson 95% confidence intervals.
- **Reporting**: Generates `llm_units.csv` and `llm_diagnosis.csv` whenever LLM candidate rows are evaluated.

---

## 6. Verification Tools

- `tools/llm_smoke.py`: Standalone CLI tool to verify live model connection and diagnosis against fault `F06` before running full pipeline sweeps.
- `--gates-only`: Flag in `pipeline/__main__.py` and `orchestrator.py` allowing validation gates V0–V3 to run and record decisions without triggering deployment or rollbacks.
