# AutoImmune

AutoImmune is a B.Tech research prototype: a hybrid self-healing pipeline for a Java Spring Boot service (order-service). It observes the service, detects and diagnoses a fault, drafts three candidate patches, and validates each one in a Docker sandbox through four gates (V0 compile, V1 target test, V2 full test suite, V3 new Semgrep findings). A rule-based risk tier then decides to REJECT, ESCALATE or AUTO_APPLY. Auto-applied patches are deployed, watched over a health window, and either promoted or rolled back, with evidence recorded for every candidate. The research question is how much execution evidence lets an AI-generated patch deploy without human review, and what each gate catches.

## Team

- Agni M N
- Pradeep S
- S Nehal

**Guide:** Mrs. M. Shona

## Documentation & Runbook

For end-to-end setup, test execution, demo procedures, and operator verification, see the complete guide:
- [Runbook](docs/RUNBOOK.md)
- [Traceability Matrix](docs/TRACEABILITY.md)
- [Phase 5 Execution Notes](docs/PHASE5_NOTES.md)
- [Phase 6 Live LLM Handoff](docs/PHASE6_HANDOFF.md)

## Pilot Results (Scripted & Rule Baseline)

> **Notice:** The current evaluation reflects a pilot evaluation across 16 scripted candidate patches across three target faults (F01, F04, F06). All labels are draft and subject to team review. Scripted and rule-based results are deterministic baselines and do not represent live LLM performance.

- **Candidate Pool:** 16 candidate units evaluated in Docker sandbox.
- **Gate Efficacy:** Each gate independently stopped unsafe patches (V1: 2, V2: 2, V3: 2).
- **Safety Policy (B3):** AUTO_APPLY candidates passed V0-V3 with zero new static analysis findings and diffs within bounds; ESCALATE routed candidates with diffs outside diagnosed file or high-risk paths to operator review.
- **Rollback Demonstration:** Verified via staged latency regression (`staged=true`), triggering automatic container rollback to the previous image tag within the health window.

## Running tests

```
.\.venv\Scripts\python -m pytest
```
