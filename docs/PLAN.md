This is the master technical specification. It must tell Antigravity what AutoImmune is, how each component works, how faults are handled, what the research experiments measure, and how we know the system is actually working.
TASK: Create the Complete AutoImmune Master Architecture and Implementation Plan
Act as a senior AI/ML research engineer, software architect, automated program repair specialist, security engineer, and experimental-methodology advisor.
Create or carefully update docs/PLAN.md in the AutoImmune repository.
This document is the authoritative master plan for implementing, validating, demonstrating, and experimentally evaluating AutoImmune.
Do not simply paste a generic architecture template. Inspect the existing repository and all relevant project instructions first. Preserve working code, align with AGENTS.md, and do not silently discard previously agreed requirements.
Write the actual Markdown file in the repository. Do not implement the entire application during this documentation task.
1. Project Definition
Define AutoImmune as an AI-assisted self-healing software system that:
1.	Observes a running target application.
2.	Detects reproducible software failures.
3.	Collects incident evidence.
4.	Diagnoses probable root causes.
5.	Generates candidate source-level repairs.
6.	Validates candidates in an isolated environment.
7.	Assesses repair risk using validation and diagnosis evidence.
8.	Rejects, escalates, or permits eligible repairs.
9.	Deploys approved repairs under controlled conditions.
10.	Monitors recovery and rolls back when necessary.
11.	Records evidence for reproducibility and research evaluation.
The main research emphasis is not simply generating patches. It is evaluating evidence-based, risk-aware repair decisions and the trade-off between safety, human intervention, and validation cost.
Explain that a working prototype and a research contribution are different deliverables. The prototype provides the experimental system; the contribution must be supported by controlled comparisons and measured results.
2. Architecture and Technology Decisions
Use the following as the default architecture unless inspection reveals an existing compatible implementation:
Orchestrator
Python 3.11 or a compatible configured version.
Responsibilities:
•	Monitoring and incident detection.
•	Incident and evidence schema validation.
•	Diagnosis and patch-generation provider integration.
•	Git diff processing.
•	Docker sandbox orchestration.
•	Validation result aggregation.
•	Risk tiering and decision logic.
•	Human approval workflow.
•	Deployment and rollback control.
•	Evidence persistence.
•	Experiment execution and statistical analysis.
Recommended tools include Typer for a CLI, pytest for tests, Python's subprocess module for trusted process orchestration, SQLite for structured experimental records, and JSON/JSONL for portable artifacts.
Do not introduce FastAPI or a web dashboard unless it materially improves the required demonstration. The CLI is sufficient for the initial implementation.
Target Application
Initially use Java 17, Spring Boot 3, and Maven for an order-service example.
Include:
•	REST endpoints with deterministic business behaviour.
•	Structured logs and useful exception traces.
•	Health reporting.
•	Visible unit and integration tests.
•	Reproducible fault fixtures.
•	A stable known-good baseline.
Keep the design sufficiently modular that a Python/FastAPI target or another repository could be supported later through a target-adapter interface.
Validation Environment
Use Docker for candidate validation. Use --network none, bounded resources, process timeouts, controlled mounts, and no exposed Docker socket or secrets.
Document any local Docker, Java, Maven, Python, or operating-system requirements.
Evidence Storage
Use:
•	JSON files for individual incident, diagnosis, gate, and decision artifacts.
•	JSONL as an append-only master evidence stream.
•	SQLite where structured experiment queries and repeatable reporting are beneficial.
Do not store only a dashboard summary that cannot be traced back to the underlying run records.
3. System Architecture Diagram
Include a valid Mermaid diagram showing:
•	Target application and its logs/health endpoints.
•	Detector and incident creation.
•	Fixed-sequence Python orchestrator.
•	Provider abstraction.
•	Diagnosis and patch generation.
•	Candidate patch store.
•	Isolated Docker sandbox.
•	V0–V3 validation.
•	Risk and decision engine.
•	Human approval.
•	Staged deployment.
•	Post-deployment monitoring.
•	Rollback and promotion.
•	Evidence recording and statistical analysis.
Use the following conceptual flow:
Target Application → Observe/Detect → Incident → Diagnose → Generate Candidate → Validate → Decide → Deploy/Escalate/Reject → Monitor → Promote/Rollback → Record.
The diagram must distinguish the sandbox validation path from the actual deployment path.
The LLM must not control the orchestrator's sequence or bypass safety gates.
4. Canonical End-to-End Pipeline
Define every stage and its inputs, outputs, errors, and responsibilities.
Stage 1: Observe
Collect logs, health-check results, functional probe results, and available latency/error metrics.
Use bounded polling or another explicitly documented monitoring mechanism. Define polling intervals and timeouts in configuration rather than scattering unexplained constants across modules.
Stage 2: Detect
Support at least:
•	Repeated application exceptions or HTTP 500 responses.
•	Failed health checks.
•	Functional probes that return incorrect business results despite HTTP 200.
•	Relevant regression signals when explicitly enabled.
Document thresholds, deduplication, incident IDs, healthy-state behaviour, and false-positive prevention.
Stage 3: Diagnose
Provide the incident evidence and bounded source context to the configured provider.
Require structured output with:
•	Ranked probable causes, capped at three.
•	Supporting evidence and source locations where available.
•	A confidence field only when its semantics are explicitly defined.
•	Uncertainty or disagreement indicators.
•	provider_mode.
•	Model/provider metadata when applicable.
Diagnosis confidence must not automatically be treated as a calibrated probability of correctness.
Stage 4: Generate Candidate Patches
Generate or retrieve a bounded number of candidate unified Git diffs.
For the MVP, target three candidates per incident where available.
Store every candidate separately. Record generation failures and invalid diffs rather than silently discarding them.
Check path restrictions, patch applicability, file scope, diff size, and prohibited changes before validation.
Do not allow a candidate to modify the validation harness, hidden tests, evidence labels, deployment controller, or decision policy unless the task explicitly authorizes a separate trusted change.
Stage 5: Validate
Run all candidate checks inside the sandbox using the canonical definitions below.
Stage 6: Assess Risk
Use explicit evidence fields and a deterministic, configurable decision policy.
The initial risk tier must be low, medium, or high.
A numerical heuristic may be added for ranking candidates, but label it as a heuristic unless it has been calibrated and evaluated on suitable labelled data.
Stage 7: Decide
Return one of:
•	REJECT
•	ESCALATE
•	AUTO_APPLY
The decision engine must be deterministic for identical inputs and identical policy versions.
Stage 8: Deploy
Deploy only candidates eligible under the policy and, when required, explicitly approved by a human.
Use an isolated staged artifact or container image where practical.
Stage 9: Monitor and Recover
Run bounded post-deployment health and functional checks.
Monitor the configured observation window and latency thresholds. If a critical breach occurs, restore the previous known-good deployment artifact.
Stage 10: Record
Record all inputs, outputs, gate results, decisions, timing information, deployment results, rollback outcomes, and evaluator labels in their appropriate stores.
5. Authoritative Validation Gate Definitions
These definitions must be used consistently across the code, tests, reports, and other documentation.
V0 — Patch Integrity and Compilation
•	Parse and validate the unified diff.
•	Reject unsafe or prohibited file paths.
•	Verify the patch applies to the expected baseline.
•	Apply it inside the isolated workspace.
•	Compile the target application using its configured build tool.
•	Capture exit codes, diagnostics, duration, and artifact references.
A patch that cannot be safely applied or compiled fails V0.
V1 — Target Reproduction Test
•	Execute visible tests that reproduce the incident.
•	Verify the intended behaviour has been restored.
•	Include functional assertions, not merely process-start checks.
•	Record pass/fail and relevant diagnostic output.
Passing V1 does not prove the patch is free of regressions.
V2 — Regression Test Suite
•	Run the permitted existing unit and integration suite.
•	Verify that previously working behaviour remains intact.
•	Record test counts, failures, skips, errors, and runtime.
Do not expose hidden ground-truth tests to the candidate validation process.
V3 — Static Analysis and Security
•	Run configured Semgrep rules (config/semgrep.yml) against baseline and patched code. SpotBugs with FindSecBugs is deferred.
•	Record tool availability, versions, findings, and severity.
•	Compare results against the same tools run on the unpatched baseline.
•	Count newly introduced findings separately from pre-existing findings.
•	Treat a missing mandatory tool or failed scan as an explicit error, not success.
Separate Runtime Validation
Define runtime replay, staging health checks, functional probes, and latency monitoring as additional runtime validation stages.
Do not redefine V3 as traffic replay.
A runtime validation result must include the relevant health status, observation window, probe outcomes, latency measurements when available, and failure reason.
Document what each gate can and cannot establish. Never claim that passing all gates guarantees the absence of unsafe behaviour.
6. Fault Catalogue and Reproducibility
Create a canonical fault catalogue for F01–F06.
At minimum, define these initial scenario categories:
•	F01 — Regression defect: A proposed fix resolves the incident but breaks an existing behaviour, such as legacy response serialization.
•	F02 — Incomplete repair: A candidate addresses only part of the original failure and leaves the reproduction test failing.
•	F03 — Invalid patch or build defect: A candidate introduces a malformed diff, invalid source change, or compilation failure.
•	F04 — Configuration/health failure: A reproducible configuration defect causes the application to become unhealthy.
•	F05 — Security regression: A candidate introduces a prohibited vulnerability, such as unsafe SQL construction, detected by configured checks or tests.
•	F06 — Wrong business result: An endpoint returns HTTP 200 with an incorrect deterministic calculation or payload, detectable by a functional probe.
These are the proposed canonical categories. If existing repository fixtures already assign different meanings to F01–F06, inspect them first and preserve working identifiers or document an explicit migration. Do not silently remap existing faults.
For every fault, document:
•	Fault ID and description.
•	Known-good behaviour.
•	Fault-introduction mechanism.
•	Observable symptoms.
•	Detection mechanism.
•	Expected root cause.
•	Visible reproduction tests.
•	Relevant regression tests.
•	Expected gate outcomes for representative candidate types.
•	Expected safe and unsafe candidate labels.
•	Rollback or recovery expectations.
•	Limitations of the scenario.
Store source-level fault introductions as Git diffs where practical.
Use hidden tests only for post-validation ground-truth labelling. Never expose them to the provider, patch generator, or validation sandbox.
Do not claim that every fault must always be detected by a specific gate if the outcome depends on the candidate. Define expected behaviour for concrete candidate fixtures instead.
7. Decision Engine
Document the following deterministic policy.
REJECT
Reject if any of the following applies:
•	V0, V1, or V2 fails.
•	A prohibited or newly introduced high-severity security finding exists.
•	The patch violates path, file-scope, or size policies that are defined as hard restrictions.
•	Mandatory evidence is missing or invalid.
•	A mandatory validation check fails or times out.
ESCALATE
Escalate when mandatory checks pass but review is required because of:
•	New lower-severity findings.
•	Diagnosis disagreement.
•	Out-of-scope but permitted changes.
•	Configured size-limit warnings.
•	Incomplete uncertainty evidence.
•	Other explicit policy-defined review conditions.
AUTO_APPLY
Auto-apply only when:
•	All mandatory checks pass.
•	No prohibited findings exist.
•	Patch scope and size meet policy.
•	Evidence is complete.
•	Required diagnosis and risk conditions are satisfied.
•	The deployment controller has a verified rollback path.
•	The policy explicitly permits automatic deployment.
Document rule precedence. A mandatory rejection condition always overrides a low risk score.
The MVP must use a rule-based risk tier. If a numerical Patch Risk Score (PRS) is implemented before adequate labelled data exists, identify it as a heuristic index and document the chosen weights, rationale, and limitations.
8. Research Questions and Hypotheses
Refine the project into experimentally testable questions.
RQ1 — Human Review and Unsafe Deployment
Under what evidence-based decision conditions can human review be reduced while keeping unsafe deployments within a predefined tolerance?
Define unsafe deployment using evaluator ground truth and the configured runtime evaluation criteria.
Measure both human intervention and unsafe deployment. Do not claim safety from a small sample without uncertainty estimates.
RQ2 — Calibration of Patch Risk
Can compilation, target tests, regression results, static-analysis findings, runtime checks, and diagnosis uncertainty predict the probability that a candidate patch is unsafe?
Distinguish:
•	A deterministic rule-based risk tier.
•	An arbitrary weighted heuristic.
•	A model output that ranks risk.
•	A statistically calibrated estimate of P(unsafe | evidence).
Only call the PRS a calibrated probability after fitting and evaluating an appropriate calibration method on held-out data.
If the labelled dataset is too small, use a transparent heuristic and report calibration as future work or an exploratory experiment.
Avoid data leakage between training, calibration, and test partitions. Prefer splitting by fault scenario or fault family where possible, rather than randomly splitting near-duplicate candidates.
RQ3 — Validation Depth, Cost, and Safety
How do progressively deeper validation strategies affect:
•	Unsafe deployment rate.
•	False rejection rate.
•	Human intervention rate.
•	Repair success.
•	Regression detection.
•	Validation time and overall recovery time.
Measure costs directly instead of inserting assumed timings.
H1 — Diagnosis Uncertainty
Hypothesis: incorporating diagnosis disagreement or uncertainty into the decision policy may reduce unsafe automatic deployments, potentially at the cost of additional escalations.
Compare the policy with and without the uncertainty feature on the same candidate fixtures and fault scenarios.
Treat the hypothesis as unproven until evaluated.
9. Baselines and Fair Comparison
Define at least these baselines:
•	B0 — Human-reviewed deployment: Every eligible candidate requires human approval after the documented validation process. Record human intervention and any unsafe outcomes; do not assume its unsafe deployment rate is mathematically zero.
•	B1 — Target-test-only policy: Uses V0 and V1 as mandatory checks, then follows a predefined permissive deployment rule. Any omitted checks must be documented.
•	B2 — Fixed deterministic policy: Uses fixed mandatory validation rules and fixed thresholds without an evidence-calibrated model.
•	B3 — AutoImmune evidence-based policy: Uses the full configured validation evidence, diagnosis uncertainty when enabled, and the explicitly defined risk-aware decision policy.
Apply the same fault set, candidate patches, baseline version, and evaluation labels across baselines.
Separate model-assisted results from replay, scripted, and rule-based results. Report provider modes and API usage.
Document any baseline differences that prevent a strictly controlled comparison.
10. Dataset and Ground-Truth Labelling
Describe how to create a reproducible dataset of fault/candidate pairs.
Candidate categories may include:
•	Correct repairs.
•	Incomplete repairs.
•	Overfitting repairs.
•	Regression-inducing repairs.
•	Security-unsafe repairs.
•	Invalid or non-applicable patches.
Each candidate must receive a ground-truth label from independent evaluation using hidden tests, additional security checks, and the defined runtime criteria where applicable.
Specify the label schema and label provenance.
Keep evaluator labels separate from provider input and decision-time evidence. Avoid labelling a candidate safe solely because all visible tests pass.
If a label cannot be established, record it as unknown and exclude it from metrics that require a known label. Report the excluded count.
Do not invent a fixed dataset size or claim statistical adequacy without justification. Start with the available reproducible fixtures, then expand based on observed coverage and experimental requirements.
11. Metrics and Correct Definitions
Define metrics precisely and implement them using explicit denominators.
Use:
•	Unsafe Deployment Rate (UDR): Unsafe automatically deployed candidates divided by all automatically deployed candidates with known evaluation outcomes.
•	Human Intervention Rate (HIR): Incidents requiring human intervention divided by all eligible incidents processed.
•	False Rejection Rate (FRR): Ground-truth safe candidates rejected by the policy divided by all ground-truth safe candidates evaluated by that policy.
•	Repair Success Rate: Incidents successfully repaired and recovered divided by eligible incidents processed.
•	Regression Detection Rate: Ground-truth regression-inducing candidates rejected before deployment divided by all ground-truth regression-inducing candidates evaluated.
•	Validation Cost: Actual measured gate execution time and total elapsed validation time; report model usage separately where applicable.
•	Time to Detect: Time from fault activation to incident detection.
•	Time to Diagnose: Time spent producing and validating the diagnosis.
•	Time to Validate: Elapsed time across the required validation stages.
•	Time to Recover: Time from incident activation to restored healthy service.
•	Calibration Quality: Brier score, log loss where applicable, and reliability diagrams or expected calibration error when a genuine probability model is evaluated.
For every metric, document edge cases, denominator-zero handling, missing outcomes, and aggregation rules.
Report sample sizes and uncertainty where feasible. Never silently replace an undefined metric with zero.
12. Telemetry Contracts
Define the schemas and required fields for:
•	incident.json
•	diagnosis.json
•	Candidate metadata and diff references.
•	gates.json
•	decision.json
•	Deployment and rollback records.
•	evidence.jsonl
At minimum, evidence records should capture:
•	run_id
•	fault_id
•	candidate_id
•	Candidate kind and ground-truth label reference, where applicable
•	Diagnosis provider mode
•	Patch provider mode
•	Relevant timestamps and durations
•	Gate status and runtime
•	New findings and severity
•	Changed files and diff size
•	Risk tier and any numerical heuristic score
•	Decision and reasons
•	Human approval status
•	Deployment status
•	Rollback status and recovery duration
•	Evaluation label and label provenance
Use explicit schema versions and validate records. Store paths to full logs instead of placing unbounded raw output in every record.
Update dependent code and tests whenever a contract changes.
13. Repository Layout
Document a practical initial structure consistent with the actual repository. Use the following as the proposed target, adapting existing compatible conventions where necessary:
autoimmune/
├── AGENTS.md
├── README.md
├── docs/
│   ├── PLAN.md
│   └── TEAM_WORKFLOW.md
├── app/
│   └── order-service/
├── faults/
│   ├── F01/
│   ├── F02/
│   ├── F03/
│   ├── F04/
│   ├── F05/
│   └── F06/
├── pipeline/
│   ├── __init__.py
│   ├── observe.py
│   ├── detector.py
│   ├── diagnose.py
│   ├── patch_generator.py
│   ├── llm_provider.py
│   ├── sandbox.py
│   ├── decide.py
│   ├── deploy.py
│   ├── rollback.py
│   └── record.py
├── config/
│   └── decision.yaml
├── cache/
├── runs/
├── tests/
├── hidden_tests/
├── evidence.jsonl
├── analyse.py
└── pyproject.toml
The layout is a guide, not permission to duplicate existing modules or move files unnecessarily. Keep hidden tests outside sandbox-mounted paths.
14. Definition of the MVP and Acceptance Criteria
Define implementation completeness in terms of working behaviour, not the number of files created.
Use the following ten acceptance checks as the initial demonstration standard:
•	A1 — End-to-end execution: A documented CLI command completes the pipeline on at least three distinct controlled fault scenarios.
•	A2 — Detection: Incidents are detected within the configured time limit, and a healthy-state test does not generate false incidents under the specified test conditions.
•	A3 — Diagnosis: Valid structured diagnosis output, ranked causes, provider mode, and top-three diagnosis evaluation are recorded.
•	A4 — Candidate generation: Up to three candidates are saved per incident where available, with invalid candidates and generation failures explicitly recorded.
•	A5 — Isolation: V0–V3 execute in a Docker sandbox with network disabled and a tested network-isolation assertion.
•	A6 — Gate differentiation: Representative candidate fixtures demonstrate that V1, V2, and V3 can each detect their intended failure class.
•	A7 — Deterministic decisions: All decision branches have unit tests and produce traceable decision artifacts.
•	A8 — Human approval: An escalated candidate can be explicitly approved or rejected, and an eligible low-risk candidate follows the configured automatic path.
•	A9 — Recovery and rollback: A healthy staged deployment is promoted, while a controlled unhealthy deployment restores the previous known-good version.
•	A10 — Evidence and analysis: The analysis script regenerates evaluation tables from saved evidence without inventing missing results.
The 80% demonstration target is at least eight genuinely passing checks out of ten, with the individual results disclosed. Critical safety failures must be reported separately and must not be excused by reaching eight checks.
Define exact commands, preconditions, expected artifacts, and observable pass conditions for each check.
15. Implementation Phases
Provide ordered implementation phases with dependencies, affected files, tests, and acceptance criteria.
At minimum:
1.	Repository and environment setup.
2.	Target application and known-good baseline.
3.	Reproducible source-level fault fixtures.
4.	Monitoring and incident detection.
5.	Provider abstraction and offline replay/scripted modes.
6.	Diagnosis schema and candidate patch storage.
7.	Isolated sandbox and V0–V3.
8.	Deterministic risk and decision engine.
9.	Approval, staged deployment, health monitoring, and rollback.
10.	Evidence recording and statistical analysis.
11.	Controlled baseline experiments.
12.	Optional calibrated risk modelling and diagnosis-uncertainty experiments.
13.	Optional web control center and additional target adapters.
For every phase include:
•	Objective.
•	Inputs and dependencies.
•	Concrete deliverables.
•	Expected files/modules.
•	Implementation notes.
•	Tests to run.
•	Definition of done.
•	Acceptance commands.
•	Failure conditions that must be fixed before continuing.
Do not impose artificial calendar deadlines. Prioritize functional dependencies and reliable verification.
16. Cost and Operational Constraints
Prefer tools that can run locally.
Require the project to demonstrate a complete scripted/replay workflow without an API key.
Keep live providers optional. Record external calls, errors, token usage when available, and estimated monetary cost only when supported by actual provider usage/pricing data.
Do not claim a provider is free or available at a particular quota without verification.
Do not require training a large model from scratch.
17. Demonstration Procedure
Write a reproducible professor-facing demo sequence:
1.	Show the healthy target application.
2.	Inject a source-level fault using the controlled fixture workflow.
3.	Show the detector's incident artifact.
4.	Show diagnosis and provider mode.
5.	Show candidate diffs.
6.	Show isolated V0–V3 validation results.
7.	Show the deterministic decision and reasons.
8.	Demonstrate human approval for an escalated candidate.
9.	Demonstrate an eligible repair deployment.
10.	Trigger a controlled post-deployment failure and show rollback.
11.	Confirm restored health.
12.	Open the saved evidence and regenerate the analysis report.
Distinguish live model execution from scripted or replay execution during the demo.
Do not hardcode successful outcomes or expected scores merely to make the demonstration appear successful. Faults and fixtures must genuinely produce the displayed results.
18. Research Limitations and Reporting Rules
Explicitly document these limitations:
•	Passing visible tests does not establish patch safety.
•	A small controlled fault set may not generalize to real production applications.
•	A heuristic risk score is not a calibrated probability.
•	Scripted providers demonstrate pipeline integration, not live-LLM repair capability.
•	Rollback can reduce recovery time but does not prevent every harmful side effect.
•	A low observed unsafe deployment rate with a small sample does not prove a stringent safety guarantee.
•	Novelty claims require a documented literature review and comparison with related systems.
Separate implemented capabilities, planned work, hypotheses, and measured results.
19. Required Output
Create docs/PLAN.md with clear headings, concise technical explanations, valid Markdown tables, valid Mermaid diagrams, consistent names, and precise acceptance criteria.
Do not leave contradictory gate definitions, placeholder citations, fabricated results, or unresolved policy conflicts in the final document.
If a requirement cannot be implemented or validated with the current repository, record it as an open issue rather than claiming it is complete.
Acceptance Criteria
The task is complete only when:
1.	docs/PLAN.md exists at the correct path.
2.	The architecture and pipeline stages are fully documented.
3.	V0–V3 definitions are consistent and unambiguous.
4.	All six fault categories are documented without silently overwriting existing fixture meanings.
5.	The decision policy has explicit precedence and safe failure behaviour.
6.	Research questions and metrics are experimentally testable.
7.	Provider modes, telemetry, and hidden-test separation are defined.
8.	The repository layout and implementation phases are actionable.
9.	All ten MVP acceptance checks have measurable pass conditions.
10.	The plan agrees with AGENTS.md.
11.	The document distinguishes implemented features from proposed features and unproven hypotheses.
12.	A completion report lists the file path, validation performed, and unresolved questions.
Do not begin implementing the full pipeline as part of this task.
