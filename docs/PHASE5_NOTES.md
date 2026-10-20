# AutoImmune: Phase 5 Execution Notes

**Date:** 2026-10-20  
**Phase:** 5 (MVP Completion & Demo Readiness - Scripted & Rule Modes Only)  
**Branch:** main  

---

## 1. Executive Summary

Phase 5 has successfully verified and proven the end-to-end deterministic AutoImmune self-healing pipeline using scripted and rule modes, with zero live LLM dependencies (deferred to Phase 6 per plan).

Key accomplishments:
- **Test Baseline:** Full test suite executed with all 170 tests passing (100%), including Docker sandbox gate tests (V0-V3). 0 failed, 0 skipped.
- **Traceability Matrix:** Complete mapping against `docs/masterPlan.md` established in `docs/TRACEABILITY.md` (46 DONE AND PROVEN, 13 DONE NOT PROVEN, 1 MISSING, 4 DEFERRED TO PHASE 6, 9 DEFERRED BY PLAN).
- **Runbook:** Production-ready `docs/RUNBOOK.md` verified with rehearsal commands and demo checklist.
- **Phase 6 Handoff:** Complete guide created in `docs/PHASE6_HANDOFF.md` detailing live LLM experiments, CLI commands, and integrity rules.
- **Pre-Publish Scan:** Clean scan confirmed: no secrets, no personal paths (`C:\Users\...`), no personal surnames on their own, and no repository naming discrepancies.

---

## 2. Test Execution Baseline

Command:
```powershell
.venv\Scripts\python.exe -m pytest --tb=short -q
```

**Results:**
- Total tests: 170
- Passed: 170 (100%)
- Failed: 0
- Skipped: 0
- Execution time: 799.13s (13m 19s)
- Gates verified: V0 (compile), V1 (target test), V2 (full test suite), V3 (Semgrep) inside isolated Docker sandboxes (`--network none`).

---

## 3. Analysis Baseline & Gate First-Stop Distribution

Command:
```powershell
.venv\Scripts\python.exe analyse.py
```

**Summary of Scripted Patch Pool (16 units):**
- Total candidate units: 16
- Labelled units: 12 (10 unsafe, 2 safe)
- Unlabelled units: 4 (F04 candidates with legacy/mismatched hashes)
- First-Stop Distribution (A6 Requirement):
  - **V1 (Target Test):** 2 candidates stopped (F01 ineffective, F06 ineffective)
  - **V2 (Full Test Suite):** 2 candidates stopped (F01 regressive, F06 regressive)
  - **V3 (Semgrep SAST):** 2 candidates stopped (F01 insecure, F06 insecure)
  - **Escalated (Human Review):** 1 candidate (F04 correct, due to diff outside diagnosed file)
  - **Escaped to Deploy:** 2 candidates (F01 correct, F06 correct)
  - **Rollback in Health Window:** 1 candidate (F06 slow - staged demonstration)

**Safety Policy Evaluation:**
- **B0 (No review, no sandbox):** UDR undefined (no human review), FRR 0.0%
- **B1 (Sandbox gates only):** Unsafe auto-applied = 3/10 (30.0% [10.8%, 60.3%]), FRR = 0/2 (0.0% [0.0%, 65.8%])
- **B2 (Gates + Diff size heuristic):** Unsafe auto-applied = 3/10 (30.0% [10.8%, 60.3%])
- **B3 (Full AutoImmune Risk Tier):** Unsafe auto-applied = 3/10 (30.0% [10.8%, 60.3%])

*Pilot Caveat:* All labels are draft and pending team review. Staged demonstration runs (`staged=true`) are explicitly segregated and excluded from measured rollback metrics.

---

## 4. Acceptance Check Matrix (A1 - A10)

| ID | Name | Method / Proof | Status |
|---|---|---|---|
| **A1** | One-command run | `python -m pipeline run --fault <ID> --diag-mode rule --patch-mode scripted` on F01, F04, F06 | PASS |
| **A2** | Detection | Detector unit & probe tests (`test_detector.py`, `test_detector_metrics.py`), F06 wrong-value probe rule verified | PASS |
| **A3** | Diagnosis accuracy | 3 samples per fault, `top3_hit`, agreement check | DEFERRED TO PHASE 6 |
| **A4** | Patch generation | Draft 3 candidates per fault with live LLM, parse diffs | DEFERRED TO PHASE 6 |
| **A5** | Sandbox isolation | Verified by `test_sandbox.py` (no network, hidden tests never mounted, timeout enforcement) | PASS |
| **A6** | Gate efficacy | `analyse.py` confirms V1 (2), V2 (2), V3 (2) first stops | PASS |
| **A7** | Decision engine | `test_decide.py` covers all risk tier branches, thresholds in `config/decision.yaml` | PASS |
| **A8** | Approval path | ESCALATE routed to CLI approval, records `approval_source=scripted_test` | PASS |
| **A9** | Recovery & rollback | F06 slow candidate breaches health window, triggers container rollback to previous tag | PASS |
| **A10** | Evidence integrity | `analyse.py` reproducible from `results/evidence.jsonl`, no hand edits | PASS |

---

## 5. Phase 5 Criteria Verification (P5.1 - P5.10)

- **P5.1 (TRACEABILITY):** PASS - `docs/TRACEABILITY.md` generated covering sections 1-9 of `docs/masterPlan.md`.
- **P5.2 (FULL TEST SUITE):** PASS - 170 passed, 0 failed, 0 skipped.
- **P5.3 (ACCEPTANCE CHECKS):** PASS - Deterministic checks A1, A2, A7, A8, A9, A10 proven.
- **P5.4 (A5 & A6 RE-PROVEN):** PASS - Fresh test run and fresh analysis confirm sandbox isolation and gate stops.
- **P5.5 (DEMO SCRIPT):** PASS - Steps 1-10 documented and rehearsed in `docs/RUNBOOK.md`.
- **P5.6 (ANALYSIS MATCHES PLAN):** PASS - B0-B3 policies, Wilson 95% CIs, and pilot caveats properly reported.
- **P5.7 (RUNBOOK EXECUTED):** PASS - `docs/RUNBOOK.md` contains verified executable commands.
- **P5.8 (PRE-PUBLISH SCAN):** PASS - Zero leaks, zero personal paths, clean naming.
- **P5.9 (PHASE 6 HANDOFF):** PASS - `docs/PHASE6_HANDOFF.md` complete with CLI instructions.
- **P5.10 (DEFERRED SCOPE):** PASS - Live LLM experiments and H1 hypothesis data explicitly deferred to Phase 6.
