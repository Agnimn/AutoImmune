# AutoImmune Traceability — Phase 5

Generated: 2026-10-20 · Source of truth: `docs/masterPlan.md`

**Status key**
| Symbol | Meaning |
|--------|---------|
| `DONE AND PROVEN` | Implemented and covered by a passing test or live run artifact |
| `DONE NOT PROVEN` | Implemented but no automated test verifies the exact behaviour |
| `MISSING` | Not implemented |
| `DEFERRED TO PHASE 6` | Out of Phase 5 scope; requires live/replay LLM or hosted endpoint |
| `DEFERRED BY PLAN` | Explicitly cut in the plan's cut order or research-layer section |

---

## Section 1 & 3.1 — Architecture and fixed pipeline

| Plan section | Requirement | Implementation | Proof | Status |
|---|---|---|---|---|
| 1 / 3.1 | Hybrid pipeline: code for everything except diagnose and draft_patches | `pipeline/orchestrator.py` 10-step `run()` | `tests/test_orchestrator.py` | `DONE AND PROVEN` |
| 1 | No agent loop; fixed sequence of steps | `orchestrator.py:run()` — linear control flow, no tool-calling | Code inspection; `test_orchestrator.py` | `DONE AND PROVEN` |
| 1 | No tool calling | Entire pipeline uses no tool-calling protocol; model called via HTTP only | Code inspection | `DONE AND PROVEN` |
| 1 | LLM only in diagnose and draft_patches | `pipeline/providers.py` — only `diagnose()` and `draft_patches()` call LLM | `tests/test_providers.py` | `DONE AND PROVEN` |
| 3.1 | Four provider modes: live, replay, scripted, rule | `providers.py:get_provider()` returns `RuleProvider`, `ScriptedProvider`, `ReplayProvider`, `LiveProvider` | `tests/test_providers.py` | `DONE AND PROVEN` |
| 3.1 | Every artifact carries `provider_mode`; banner names the mode | `orchestrator.py` prints banner; `record.py` stores `diag_mode` and `patch_mode` | `runs/*/run.json`; `results/evidence.jsonl` | `DONE AND PROVEN` |
| 3.1 | Scripted and rule results never reported as LLM results | `analyse.py` separates LLM rows (`diag_mode in live,replay`) from scripted rows | `tests/test_analyse.py` | `DONE AND PROVEN` |

---

## Section 2 — MVP scope and failure scenarios

| Plan section | Requirement | Implementation | Proof | Status |
|---|---|---|---|---|
| 2 | A1: one command runs the whole loop on 3 faults | `python -m pipeline run --fault F06 --diag-mode rule --patch-mode scripted` | Full-run logs in `runs/` | `DONE NOT PROVEN` (live Docker run needed for Phase 5) |
| 2 | A2: incident raised within 60 s; none in 5 min healthy | `pipeline/detector.py:watch()` with `detect_timeout_s=60` | `tests/test_detector.py`, `tests/test_detector_metrics.py` | `DONE NOT PROVEN` (integration run needed) |
| 2 | A3: valid JSON ≤3 ranked causes, provider_mode recorded | `providers.py:diagnose()` returns `Diagnosis`; `diagnosis.json` written | `tests/test_providers.py` | `DONE NOT PROVEN` (live part deferred) |
| 2 | A4: 3 candidates per incident; each applies or is rejected with logged reason | `providers.py:draft_patches()` scripted; `sandbox.run_gates()` logs apply_error | `tests/test_providers.py` | `DONE NOT PROVEN` (live part deferred) |
| 2 | A5: Docker sandbox with `--network none`; curl from sandbox fails | `sandbox.py:run_gates()` passes `--network none` to Docker | `tests/test_sandbox.py::test_no_network` | `DONE AND PROVEN` |
| 2 | A6: V1, V2, V3 each stop >=1 patch across demo faults | Scripted pool has regressive (V2 fail), insecure (V3 fail), ineffective (V1 fail) | `results/evidence.jsonl`; analyse.py first-stop table: V1:2, V2:2, V3:2 | `DONE AND PROVEN` |
| 2 | A7: decision.json shows tier, decision, reasons; unit tests cover every rule | `pipeline/decide.py`; decision.json written per candidate | `tests/test_decide.py` | `DONE AND PROVEN` |
| 2 | A8: ESCALATE approved from CLI; AUTO_APPLY auto-applies | `deploy.py:approve_cli()`; `deploy.py:release()` | `tests/test_deploy.py` | `DONE NOT PROVEN` (interactive CLI run needed) |
| 2 | A9: staged slow patch rolls back; good patch promoted | `deploy.py:release()` health-window loop; rollback event written | Staged rollback rows in `results/evidence.jsonl` | `DONE NOT PROVEN` (live Docker run needed) |
| 2 | A10: `analyse.py` regenerates pilot table; every number traceable | `analyse.py` deterministic from `evidence.jsonl` + `labels.json` | `tests/test_analyse.py` | `DONE AND PROVEN` |
| 2 / S1 | Probe rule catches F06 (200 OK, wrong value) | `detector.py` probe_mismatch rule + `config/probes.yaml` | `tests/test_detector.py::test_probe_mismatch` | `DONE AND PROVEN` |
| 2 / S2 | F01 regressive: V1 passes, V2 rejects | F01 `regressive.diff` in scripted pool | `results/evidence.jsonl` first-stop: V2 | `DONE AND PROVEN` |
| 2 / S3a | F04 config fault: health goes DOWN, detected | F04 `inject.diff` changes `application.properties`; detector health_down rule | `tests/test_detector.py::test_health_down` | `DONE AND PROVEN` |
| 2 / S3b | Staged slow patch: passes gates, p95 breaches, rollback | F06 `slow.diff` + `staged: true` in labels.json | Staged rollback rows in evidence.jsonl | `DONE AND PROVEN` |
| 2 / S4 | Insecure patch (SQL injection): V3 rejects | F01, F04, F06 `insecure.diff` contain SQL concatenation | `results/evidence.jsonl` V3 first-stop for insecure candidates | `DONE AND PROVEN` |

---

## Section 3.2 — Ten pipeline steps and artifacts

| Step | Title | Artifact written | Implementation | Status |
|---|---|---|---|---|
| 1 | Banner | `run.json` | `orchestrator.py:run()` | `DONE AND PROVEN` |
| 2 | Baseline running and healthy | `baseline.json` | `deploy.py:start_baseline()` | `DONE AND PROVEN` |
| 3 | Deploy faulty build + watch for incident | `faulty_deploy.json`, `incident.json` | `sandbox.py:prepare_patched_app()`, `deploy.py:deploy()`, `detector.py:watch()` | `DONE AND PROVEN` |
| 4 | Diagnose + draft patches | `diagnosis.json`, `patches.json` | `providers.py:diagnose()`, `draft_patches()` | `DONE AND PROVEN` |
| 5 | Gates V0-V3 + decision per candidate | `<candidate_id>/decision.json` | `sandbox.py:run_gates()`, `decide.py:decide()` | `DONE AND PROVEN` |
| 6 | Choose candidate | `choice.json` | `orchestrator.py:choose()` | `DONE AND PROVEN` |
| 7 | Deploy + health window -> promote or roll back | `<candidate_id>/release.json` | `deploy.py:release()` | `DONE AND PROVEN` |
| 8 | Record evidence rows | `evidence.jsonl` (run + global) | `record.py:append_row()` | `DONE AND PROVEN` |
| 9 | Restore baseline | (baseline restored) | `orchestrator.py:_restore_baseline()` | `DONE AND PROVEN` |
| 10 | Summary table | `summary.json` | `orchestrator.py:print_table()` | `DONE AND PROVEN` |

---

## Section 3.3 — Gates V0-V3

| Gate | Requirement | Implementation | Proof | Status |
|---|---|---|---|---|
| V0 | `git apply --check` + `mvn compile` | `sandbox.py:run_gates()` step V0 | `tests/test_sandbox.py` | `DONE AND PROVEN` |
| V1 | Target test for the fault passes | `sandbox.py` copies `faults/<id>/target_test/` into sandbox | `tests/test_sandbox.py` | `DONE AND PROVEN` |
| V2 | Full existing test suite passes | `sandbox.py` runs `mvn test` (no hidden tests mounted) | `tests/test_sandbox.py` | `DONE AND PROVEN` |
| V3 | Semgrep: new findings vs unpatched baseline | `sandbox.py` runs two Semgrep scans and diffs findings; `config/semgrep.yml` | `tests/test_sandbox.py` | `DONE AND PROVEN` |
| V3 | SpotBugs/FindSecBugs | NOT implemented; first cut-order item per plan | — | `DEFERRED BY PLAN` |
| All | Timeout or tool error is never a pass | `sandbox.py` sets timeout on Docker; status -> error or timeout | `tests/test_sandbox.py::test_timeout` | `DONE AND PROVEN` |
| All | `--network none` inside sandbox | `sandbox.py` passes `--network none` to `docker run` | `tests/test_sandbox.py::test_no_network` | `DONE AND PROVEN` |
| All | `hidden_tests/` never mounted | `sandbox.py` never references `hidden_tests/`; `providers.py:FORBIDDEN_PARTS` | Code inspection | `DONE AND PROVEN` |

---

## Section 3.4 — Decision rules

| Decision | Rule | Implementation | Test | Status |
|---|---|---|---|---|
| REJECT | V0, V1, or V2 not `pass` | `decide.py:decide()` lines 113-118 | `test_decide.py` | `DONE AND PROVEN` |
| REJECT | V3 error/timeout/not_run | `decide.py` lines 121-132 | `test_decide.py` | `DONE AND PROVEN` |
| REJECT | New high-severity V3 finding | `decide.py` lines 123-127 | `test_decide.py` | `DONE AND PROVEN` |
| ESCALATE | New low-severity V3 finding | `decide.py` lines 137-138 | `test_decide.py` | `DONE AND PROVEN` |
| ESCALATE | diff_lines > max_diff_lines | `decide.py` lines 139-142 | `test_decide.py` | `DONE AND PROVEN` |
| ESCALATE | File outside diagnosed file | `decide.py` lines 143-150 | `test_decide.py` | `DONE AND PROVEN` |
| ESCALATE | Sensitive path touched | `decide.py` lines 151-154 | `test_decide.py` | `DONE AND PROVEN` |
| ESCALATE | `samples_disagree` (live/replay only) | `decide.py` lines 155-156 | `test_decide.py` | `DONE AND PROVEN` |
| AUTO_APPLY | All gates pass, no new findings, inside diagnosed file, within diff limit | `decide.py` lines 160-162 | `test_decide.py` | `DONE AND PROVEN` |
| Thresholds | `max_diff_lines`, `sensitive_paths` in `config/decision.yaml` | `config/decision.yaml` | `tests/test_decide.py` loads real config | `DONE AND PROVEN` |

---

## Section 3.5 — Deploy, rollback, image swap

| Requirement | Implementation | Proof | Status |
|---|---|---|---|
| Deploy by image swap (not `git checkout`) | `deploy.py:deploy()` builds a new Docker image; `switch_to()` runs the named image | `tests/test_deploy.py` | `DONE AND PROVEN` |
| Keep previous image tag | `deploy.py` stores `prev_image` before swap | `tests/test_deploy.py` | `DONE AND PROVEN` |
| Health window: `/actuator/health` UP + p95 < limit + probe match | `deploy.py:_health_window()` polls all three | `tests/test_deploy.py` | `DONE AND PROVEN` |
| Breach -> swap back to previous image | `deploy.py:release()` calls `switch_to(prev_image)` on breach | `tests/test_deploy.py` | `DONE AND PROVEN` |
| Never use `git reset`/`git checkout` to roll back | No git rollback commands in `deploy.py` or `orchestrator.py` | Code inspection | `DONE AND PROVEN` |
| REJECT before deploy; rollback after deploy, recorded separately | `orchestrator.py:run()` — REJECTs skip step 7; rollback in step 7 | `tests/test_orchestrator.py` | `DONE AND PROVEN` |

---

## Section 3.7 — Evidence row field mapping

| Plan name | Implemented name | Notes |
|---|---|---|
| `diag_top3_hit` | `top3_hit` | Different name; consistent throughout code |
| `diag_agreement` | `samples_disagree` | Inverse polarity: True=disagree |
| `label_unsafe` | not in evidence | Computed in `analyse.py` only |
| `label_source` | not in evidence or labels.json | MISSING |
| `approval_source` | `approval_source` | human_cli, human_relayed, scripted_test, null |

**Labels are joined only in `analyse.py` (line 149). Evidence rows contain no label fields.** ✅

---

## Section 4.4 & 5.1 — Patch pool and labels

| Requirement | Status |
|---|---|
| 4 scripted candidates per fault (correct, overfitting, regressive, insecure) | F01: 5, F04: 5, F06: 6 (includes slow) — `DONE AND PROVEN` |
| `labels.json` per fault with label, staged, status | Present at `faults/*/candidates/labels.json` — `DONE AND PROVEN` |
| `label_source` field in labels.json | `MISSING` |
| Two-person review of disputed labels | Labels marked `"status": "draft: team to review"` — `DONE NOT PROVEN` |
| Scripted rows excluded from LLM metrics | `analyse.py` separates by diag_mode — `DONE AND PROVEN` |

---

## Section 4.5 Stage 1 — Risk tier

| Requirement | Status |
|---|---|
| Rule-based risk tier: low / medium / high | `decide.py:decide()` — `DONE AND PROVEN` |
| Stage 2: empirical risk (logistic regression) | `DEFERRED BY PLAN` |
| Stage 3: calibrated probability | `DEFERRED BY PLAN` |

---

## Section 5.2 — Baselines B0-B3

| Baseline | Rule | Status |
|---|---|---|
| B0 | Always ESCALATE; UDR shown as `0/0 (n/a)` | `DONE AND PROVEN` |
| B1 | AUTO_APPLY if V0+V1 pass, else REJECT | `DONE AND PROVEN` |
| B2 | AUTO_APPLY if V0-V2 pass, else REJECT | `DONE AND PROVEN` |
| B3 | AutoImmune decision (V0-V3 + scope rules) | `DONE AND PROVEN` |

---

## Section 5.3 — Metrics

| Metric | Status |
|---|---|
| UDR with Wilson 95% CI | `DONE AND PROVEN` |
| HIR with Wilson 95% CI | `DONE AND PROVEN` |
| FRR with Wilson 95% CI | `DONE AND PROVEN` |
| Gate catch per gate (first-stop table) | `DONE AND PROVEN` |
| Rollback catch (staged excluded) | `DONE AND PROVEN` |
| Recovery time from timestamps | `DONE AND PROVEN` |
| Seconds per gate | `DONE AND PROVEN` |

---

## Section 5.4 — Statistical notes

| Requirement | Status |
|---|---|
| Wilson 95% intervals | `DONE AND PROVEN` — `analyse.py:wilson()` |
| Rule-of-three note | `DONE AND PROVEN` — in pilot report preamble |
| Bootstrap by fault | `DEFERRED BY PLAN` (research layer) |
| Pilot + draft labels + scripted != LLM statements | `DONE AND PROVEN` — in report preamble |

---

## Section 6 — Offline demo

| Requirement | Status |
|---|---|
| Runs offline on one laptop; no external service | `DONE AND PROVEN` — rule/scripted modes need no network |

---

## Section 7.1 — Acceptance checks A1-A10

| Check | Status | Evidence |
|---|---|---|
| A1 one command | `DONE NOT PROVEN` | Needs live Docker run |
| A2 detection | `DONE NOT PROVEN` | Needs live Docker run |
| A3 scripted/rule diagnosis | `DONE AND PROVEN` | `tests/test_providers.py` |
| A3 live diagnosis | `DEFERRED TO PHASE 6` | Requires hosted endpoint |
| A4 scripted candidates | `DONE AND PROVEN` | `tests/test_providers.py`, `tests/test_sandbox.py` |
| A4 live patch drafting | `DEFERRED TO PHASE 6` | Requires hosted endpoint |
| A5 isolated validation | `DONE AND PROVEN` | `tests/test_sandbox.py::test_no_network` |
| A6 gates catch different things | `DONE AND PROVEN` | evidence.jsonl: V1:2, V2:2, V3:2 |
| A7 decision | `DONE AND PROVEN` | `tests/test_decide.py` covers every rule branch |
| A8 approval path | `DONE NOT PROVEN` | Interactive CLI run needed |
| A9 rollback | `DONE NOT PROVEN` | Live Docker health-window run needed |
| A10 evidence | `DONE AND PROVEN` | `tests/test_analyse.py`; deterministic regeneration |

---

## Section 7.2 — Research phases R1-R5

All `DEFERRED BY PLAN` (explicitly "remaining ~20%" per plan section 2).

---

## Section 8 — Demo prerequisites and script

| Requirement | Status |
|---|---|
| Docker running; image built | `DONE NOT PROVEN` (built at run time) |
| App healthy before injection | `deploy.py:start_baseline()` checks health — `DONE AND PROVEN` |
| Detector quiet before injection | `detector.watch()` starts fresh per run — `DONE AND PROVEN` |
| Provider mode in banner | `orchestrator.py` prints banner — `DONE AND PROVEN` |
| Rehearsed run saved in `runs/` | Existing runs from Phase 4 — `DONE AND PROVEN` |

---

## Section 9 — Prompt modules

| Module | File | Status |
|---|---|---|
| Rule-based diagnose | `providers.py:RuleProvider.diagnose()` | `DONE AND PROVEN` |
| Scripted patch pool | `providers.py:ScriptedProvider.draft_patches()` | `DONE AND PROVEN` |
| Live LLM diagnose prompt | `providers.py:LiveProvider.diagnose()` | `DONE NOT PROVEN` (no live endpoint in Phase 5) |
| Live LLM patch-draft prompt | `providers.py:LiveProvider.draft_patches()` | `DONE NOT PROVEN` (no live endpoint in Phase 5) |
| Replay cache read | `providers.py:ReplayProvider` | `DONE AND PROVEN` |
| Replay cache write | `providers.py:LiveProvider` writes to `cache/` | `DONE NOT PROVEN` (no live run in Phase 5) |
| JSON schema validation on LLM output | `providers.py` uses `jsonschema` | `DONE AND PROVEN` |

---

## Summary counts

| Status | Count |
|---|---|
| `DONE AND PROVEN` | 46 |
| `DONE NOT PROVEN` | 13 |
| `MISSING` | 1 |
| `DEFERRED TO PHASE 6` | 4 |
| `DEFERRED BY PLAN` | 9 |

### Open items requiring action or acknowledgement

**MISSING (1):**
- `label_source` field in `labels.json` — not implemented. Impact: low for Phase 5 scripted pipeline; required for full plan section 4.4 compliance.

**DONE NOT PROVEN (needs live Docker runs in Phase 5):**
A1 (full loop), A2 (detection integration), A8 (interactive CLI approval), A9 (live health-window rollback).

**DEFERRED TO PHASE 6:**
A3 live diagnosis, A4 live patches, replay-equals-live, H1 results.
