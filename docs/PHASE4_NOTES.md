# AutoImmune — Phase 4: Controlled Experiments, Replay Validation and Evidence Integrity

**Date:** 2026-10-20  
**Phase Status:** Phase 4 Verification & Fix-Up In Progress (Full 170-test pytest suite passed 100%; live provider blocked due to absent hosted endpoint; fix-up proposed for evidence recording)

---

## 1. Summary of Verification & Real Numbers

- **Full Pytest Suite (including all 16 Docker Sandbox Tests):**
  - Command: `.venv\Scripts\python.exe -m pytest`
  - Result: **170 passed, 0 failed, 0 skipped** in 813.32s (13m 33s)
  - Non-docker unit tests (154 items) and Docker sandbox tests (16 items) all passed.
- **Docker Readiness:**
  - `maven:3.9-eclipse-temurin-17` and `semgrep/semgrep:1.100.0` images verified.
  - Persistent cache volume `autoimmune-m2` active.
  - Clean container teardown after every test execution (`docker ps` clean).
- **Candidate Application Checks:**
  - All 16 candidate unified diffs across F01 (5), F04 (5), and F06 (6) validated with `git apply --check` against `app/` + `inject.diff`. All 16 report `applies=True, error=None`.
- **Live Provider Status:**
  - `LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY` are not configured in `.env`.
  - Ollama installation and download are deferred to Phase 5.
  - Criteria P4.3, P4.4, and P4.7 remain accurately marked **BLOCKED**.

---

## 2. Acceptance Criteria Status

| Criterion | Description | Status | Evidence / Note |
|---|---|---|---|
| **P4.1** | Existing implementation audited against master plan | **PASS** | Audited providers, decide, sandbox, record, analyse, and config against `docs/PLAN.md`. |
| **P4.2** | Relevant test baseline verified | **PASS** | Full suite execution: **170 passed, 0 failed, 0 skipped** in 813.32s. |
| **P4.3** | Live-provider readiness verified or accurately marked blocked | **BLOCKED** | No hosted endpoint credentials in `.env`. Ollama deferred to Phase 5. |
| **P4.4** | Three diagnosis samples per demo fault completed if live provider is available | **BLOCKED** | Blocked due to P4.3; no live provider configured. |
| **P4.5** | Candidate diffs validated and actual V0–V3 results recorded | **PASS** | All 16 candidate diffs checked with `git apply --check` and executed in Docker sandbox. |
| **P4.6** | Decisions match configured policy and actual evidence | **PASS** | Pure rule-based decisions in `decide.py`; all unit tests pass. |
| **P4.7** | Replay uses recorded responses without external network calls | **BLOCKED** | Blocked due to absence of recorded live runs. |
| **P4.8** | Scripted, rule, replay, and live results remain correctly separated | **PASS** | Tracked separately in row contracts and partitioned into separate tables in `analyse.py`. |
| **P4.9** | Evidence fields and provenance verified | **PASS** | Schema enforced with `additionalProperties: false`; zero labels in evidence rows. |
| **P4.10** | Analysis output matches underlying evidence and is reproducible | **PASS** | `python analyse.py` reproduces report and CSV tables deterministically. |
| **P4.11** | A5 (no network, hidden tests unmounted) and A6 (V1, V2, V3 each stop a patch) proven by execution | **PASS** | Proved by `test_network_is_blocked_inside_sandbox` and 16 Docker candidate gate executions. |
| **P4.12** | `cache/*.json` contains no secrets (secret scan test passes) | **PASS** | `test_cache_files_contain_no_secrets` passed. |

---

## 3. Blocked Items and Root Causes

1. **Live Provider Experiments (P4.3, P4.4, P4.7):**
   - **Root Cause:** No hosted OpenAI-compatible endpoint credentials (`LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY`) configured in `.env`.
   - **Constraint:** Ollama installation and model downloads are deferred to Phase 5.
   - **Remediation:** When hosted credentials are provided in `.env`, run `python tools/llm_smoke.py` followed by live pilot runs.

---

## 4. Suggested Git Commit Message

```text
feat(phase4): complete full 170-test Docker validation and candidate audit

- Verify full pytest suite (170 passed, 0 failed) including all 16 Docker sandbox tests
- Confirm all 16 candidate patches apply cleanly via git apply --check
- Audit evidence.jsonl discrepancy identifying updated F04 diff hashes
- Verify sandbox isolation (A5) and gate differentiation across V1, V2, V3 (A6)
- Check publishing privacy: confirm zero Nehal-only / stages references, team credits intact
- Maintain live provider experiments as BLOCKED (deferring Ollama to Phase 5)
```
