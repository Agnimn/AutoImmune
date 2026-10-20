This is the permanent instruction file. It tells Antigravity how to behave throughout the repository, regardless of which module it is implementing.
TASK: Create the Authoritative AGENTS.md for AutoImmune
Act as a senior software architect, AI/ML engineer, DevSecOps engineer, and research systems engineer. You are working on a final-year research project named AutoImmune, an AI-assisted self-healing software system.
Your task is to create a complete, precise, production-minded AGENTS.md file in the repository root. This file establishes the permanent rules that Antigravity and other AI coding assistants must follow while developing, testing, debugging, reviewing, and modifying AutoImmune.
Do not merely produce a suggested template in chat. Inspect the existing repository, create or update the actual file, and verify the result.
1. Initial Repository Inspection
Before modifying any files:
1.	Inspect the repository root and existing directory structure.
2.	Read existing AGENTS.md, .cursorrules, README.md, docs/PLAN.md, and docs/TEAM_WORKFLOW.md if they exist.
3.	Identify the existing programming languages, frameworks, build systems, tests, configuration files, and module boundaries.
4.	Preserve useful existing implementation and instructions.
5.	Do not overwrite unrelated work, remove files, reset Git changes, or silently discard existing rules.
6.	If an existing requirement conflicts with this task, document the conflict and apply the authoritative project requirements below.
7.	Do not implement the entire application while creating this document.
The purpose of this task is to establish repository-wide operating rules, not to build all project modules.
2. Project Identity and Architectural Principles
Document the following architectural requirements.
AutoImmune is a hybrid, evidence-driven software repair and recovery system.
Its intended workflow is:
Observe → Detect → Diagnose → Generate Candidate Repairs → Validate in Isolation → Assess Risk → Decide → Deploy or Escalate → Monitor Recovery → Roll Back if Necessary → Record Evidence.
The recommended initial technology stack is:
•	Python 3.11 or a compatible explicitly configured Python version for orchestration, monitoring, provider integration, patch processing, risk assessment, evidence recording, and experimental analysis.
•	Java 17 and Spring Boot 3 for the initial order-service target application.
•	Maven as the initial target application's build and test system, unless the existing repository already establishes another working build system.
•	Docker for isolated candidate validation.
•	Git for source control, fault fixtures, candidate patches, and controlled deployment artifacts.
•	SQLite and/or JSONL for persistent experiment data and execution evidence.
•	Pytest for Python unit and integration tests.
•	A CLI as the initial control interface. A web interface is optional and must not delay the core pipeline.
Python is the recommended orchestrator language, not a requirement that every target application must use Python or Java. Keep target-specific functionality behind explicit interfaces where practical.
Do not introduce Kubernetes, multiple independent microservices, a custom compiler, or a custom code editor unless an approved requirement demonstrates that it is necessary.
3. Strict LLM Boundaries
Large language models may be used only for these two primary operations:
1.	Failure diagnosis: receive relevant incident evidence, logs, stack traces, and bounded source context; return a structured diagnosis containing ranked causes and supporting evidence.
2.	Candidate patch generation: receive the diagnosis and relevant source context; return candidate unified Git diffs and a concise explanation.
All other pipeline operations must be controlled by ordinary deterministic software.
These include:
•	Monitoring and incident detection.
•	Schema validation and parsing.
•	Candidate count and patch-size limits.
•	Git diff validation and patch application checks.
•	Docker sandbox creation and teardown.
•	Compilation, testing, static analysis, and runtime health checks.
•	Risk tiering and final deployment decisions.
•	Human approval handling.
•	Deployment, health monitoring, rollback, and recovery.
•	Evidence collection, labelling, and statistical evaluation.
Never create an unconstrained autonomous agent loop, ReAct loop, or LLM-controlled execution sequence. The orchestrator must follow a predefined, bounded state machine. Any retries must be deterministic, explicitly configured, limited in number, and recorded.
The LLM must never independently decide to bypass validation, grant itself approval, alter safety thresholds, or execute deployment commands.
4. Provider Abstraction and Offline Operation
All model-related operations must use one documented provider abstraction.
Support four explicit provider modes:
•	live: a genuine external model API or explicitly configured local model integration.
•	replay: a response retrieved from a recorded response cache.
•	scripted: a predetermined diagnosis or candidate fixture used for controlled testing.
•	rule: a deterministic, rule-based fallback.
Do not describe these modes as interchangeable forms of AI.
Requirements:
1.	Each provider must declare its mode explicitly.
2.	Every relevant artifact must record provider_mode.
3.	Diagnostic and patch-generation modes must be recorded separately if they differ.
4.	External model responses must be parsed and schema-validated before use.
5.	Missing API keys, network failures, rate limits, timeouts, malformed JSON, and invalid patches must produce explicit errors or documented fallbacks.
6.	Replay and scripted fixtures must support a complete deterministic demonstration without API keys.
7.	The system must never label a scripted or rule-generated repair as a successful live-LLM repair.
8.	Evaluation reports must separate live, replay, scripted, and rule-based results.
9.	Secrets must be loaded from environment variables or an appropriate local secrets mechanism and must never be committed.
10.	Never hardcode experimental success rates or fabricated model performance.
Do not promise that a particular provider has a free tier or unlimited access. Keep provider adapters replaceable and document any external configuration requirements.
5. Safety and Docker Isolation
Candidate code is untrusted input.
Never compile, execute, import, or run candidate application code directly on the host as part of candidate validation.
Every candidate validation run must occur in an isolated Docker environment with:
•	--network none for the validation container.
•	No Docker socket mounted inside the candidate container.
•	No host credentials, SSH keys, API tokens, or unrelated secrets.
•	A temporary, dedicated workspace containing only the permitted source and validation fixtures.
•	Explicit CPU, memory, process, and execution-time limits where supported.
•	A non-root execution user wherever practical.
•	Read-only mounts for fixtures and tools where possible.
•	Controlled writable directories for compilation outputs and temporary files.
•	Cleanup after success, failure, timeout, and cancellation.
The sandbox must not contain hidden_tests/, hidden ground-truth labels, reference-only exploit fixtures, or evaluator-only information.
The orchestrator may run trusted Docker-control commands on the host to manage containers. However, untrusted candidate code must execute only inside the isolated validation environment.
The network-isolation acceptance check must verify actual isolation rather than merely checking that the Docker command contains a flag.
Never treat Docker alone as a complete security boundary. Document residual risks and keep host privileges minimal.
6. Fault Injection and Ground-Truth Separation
Faults must be reproducible source-level defects or controlled source/configuration diffs stored under faults/.
Do not implement benchmark faults as ordinary runtime boolean switches that simply change the target application's behaviour.
Use a consistent fault structure where appropriate:
faults/F01/, faults/F02/, and so on, containing:
•	fault.json: fault metadata and expected observable symptoms.
•	reference.diff: the source-level fault introduction.
•	target_test/: permitted visible reproduction tests.
•	hidden_tests/: evaluator-only ground-truth tests, kept outside candidate validation.
•	candidates/: labelled candidate patch fixtures, where appropriate.
The exact directory layout may be adapted to the existing repository, but its semantics must remain clear.
Faults, candidate patches, and evaluation labels must be reproducible. Preserve the known-good baseline and the original fault fixture.
Never expose hidden tests or ground-truth labels to the LLM, candidate generator, or validation sandbox.
The evaluator may use hidden tests after candidate validation to determine whether a candidate is actually unsafe or incorrect.
7. Canonical Validation Gates
Use one authoritative definition throughout the repository:
•	V0 — Patch and compilation gate: Validate patch format, path restrictions, patch applicability, and successful compilation.
•	V1 — Target reproduction gate: Run visible tests that reproduce the original incident and verify the intended repair.
•	V2 — Regression gate: Run the permitted existing unit and integration test suite to identify regressions.
•	V3 — Static-analysis and security gate: Run configured static-analysis and security tools, comparing findings against the unpatched baseline so only newly introduced findings are counted as new.
All four gates must run inside the isolated sandbox.
Runtime replay, deployment health checks, latency monitoring, and post-deployment recovery checks must be defined as separate runtime validation stages. Do not silently redefine V3 as traffic replay in one module and static analysis in another.
Each gate must produce a structured result with at least:
•	Gate identifier.
•	Pass/fail/error/timeout status.
•	Execution duration.
•	Relevant exit code.
•	A bounded diagnostic summary.
•	Artifact or log reference.
•	Tool/version metadata where available.
A failed gate is not a pass. A timeout is not a pass. An unavailable security tool must not be silently reported as a successful security scan.
8. Deterministic Risk and Decision Rules
The MVP must distinguish a rule-based risk tier from a statistically calibrated probability.
Use the following decision policy as the default:
REJECT
Reject a candidate if:
•	V0, V1, or V2 fails.
•	A new prohibited or high-severity security finding is introduced.
•	The patch violates sandbox, file-scope, or policy restrictions.
•	The patch cannot be applied safely.
•	A mandatory validation gate fails or produces an unresolved result.
ESCALATE
Require explicit human approval if mandatory checks pass but:
•	A new lower-severity finding requires review.
•	The patch exceeds configured size limits.
•	The patch touches files outside the diagnosed and approved scope.
•	Independent diagnosis results materially disagree.
•	Evidence is incomplete or uncertainty remains above the configured threshold.
•	The decision engine identifies another documented review condition.
AUTO_APPLY
Allow automatic application only if:
•	All mandatory validation gates pass.
•	No prohibited or new actionable security findings exist.
•	The patch stays within approved file and size limits.
•	Diagnosis and validation evidence satisfy configured decision requirements.
•	The configured policy explicitly permits automatic application.
•	The deployment controller can retain and restore the known-good version.
Use config/decision.yaml as the authoritative location for configurable policy thresholds and limits.
Every decision must record its action, risk tier, reasons, policy version, relevant evidence, and any failed conditions.
Do not allow a low numeric score to override a mandatory rejection condition.
Do not claim that a rule-based score is a calibrated probability. Statistical calibration is a research extension requiring sufficient labelled data and held-out evaluation.
9. Deployment and Rollback Safety
The deployment controller must:
1.	Preserve the known-good version before deployment.
2.	Deploy only a candidate that has received an eligible deterministic decision or explicit human approval.
3.	Use a separate staged deployment artifact or container image where practical.
4.	Perform bounded post-deployment health checks.
5.	Monitor configured health, functional probes, and latency thresholds during the observation window.
6.	Promote the candidate only after the required checks pass.
7.	Trigger rollback when a documented critical recovery condition occurs.
8.	Record the rollback reason, elapsed time, restored version, and recovery outcome.
Never use an unconditional git checkout ., git reset --hard, or equivalent destructive command to roll back a repair on a developer's working tree.
Rollback must restore the previously recorded deployment artifact or isolated deployment state, not erase unrelated uncommitted changes.
Deployment must default to dry-run or an explicitly controlled local environment until deployment safety checks have been verified.
Human approval must never be bypassed when the decision is ESCALATE.
10. Evidence and Data Integrity
Record every run with a unique run_id and every candidate with a unique candidate_id.
Use structured artifacts such as:
•	incident.json
•	diagnosis.json
•	Candidate unified diff files
•	gates.json
•	decision.json
•	Deployment and rollback records
•	evidence.jsonl
Each record should include applicable fault, candidate, provider-mode, validation, decision, and execution metadata.
The master evidence store must be sufficient to reproduce evaluation tables without rerunning model calls.
Never:
•	Invent results.
•	Fill missing outcomes with presumed successes.
•	Treat unexecuted checks as passed.
•	Mix hidden-test outcomes into the evidence supplied to the patch generator.
•	Mix scripted results with live-LLM results without explicit grouping.
•	Claim an unsafe deployment rate of zero without sufficient observations and an honest description of sample size and uncertainty.
Store ground-truth safety labels separately from information available to the candidate generator and decision engine.
11. Shared Repository and Team Rules
Respect the module ownership and Git workflow documented in docs/TEAM_WORKFLOW.md.
Before modifying shared interfaces:
1.	Inspect the current interface definition.
2.	Determine which modules depend on it.
3.	Propose the smallest compatible change.
4.	Update relevant schemas and tests.
5.	Update docs/PLAN.md if architecture, gate definitions, evidence schemas, or decision policy changes.
6.	Notify the team through the project's agreed coordination process.
Do not silently rename files, change JSON field names, move directories, or replace established technologies.
Do not overwrite another member's in-progress work. Do not switch branches or commit, push, merge, or rewrite Git history unless the user has explicitly requested the relevant operation.
12. Engineering Standards
•	Follow PEP 8 and use Python type hints.
•	Use clear Java naming conventions and appropriate Spring Boot practices.
•	Keep modules focused, testable, and documented.
•	Validate external input and all model output.
•	Use subprocess argument arrays rather than unsafe shell-string construction.
•	Apply timeouts to external processes and provider calls.
•	Capture useful error messages without leaking secrets.
•	Use explicit exception handling.
•	Avoid unnecessary abstractions and dependencies.
•	Add unit tests for deterministic decision logic.
•	Add integration tests for pipeline contracts and failure handling.
•	Make repeated executions reproducible where practical.
•	Pin or document relevant dependency and tool versions.
•	Do not suppress failing tests or weaken acceptance criteria merely to obtain a passing result.
13. Incremental Implementation Policy
Implement and verify one bounded module at a time.
For every implementation task:
1.	Inspect existing code and interfaces.
2.	State the intended change briefly.
3.	Make the smallest coherent implementation.
4.	Add or update tests.
5.	Execute the relevant tests and acceptance commands.
6.	Inspect failures and fix root causes.
7.	Report exactly what passed, failed, timed out, or was not executed.
8.	Stop before dependent work if a mandatory acceptance check fails.
Do not claim that a module works merely because its files exist.
Do not implement all phases at once when the task calls for incremental development.
14. Research Integrity
AutoImmune is both a software prototype and an empirical research project.
The research concerns:
•	When human review may be reduced without exceeding a defined unsafe-deployment tolerance.
•	Whether validation evidence can support a calibrated estimate of patch risk.
•	How validation depth trades off against execution cost, false rejection, and unsafe deployment.
•	Whether diagnosis uncertainty improves risk-aware decisions.
Treat these as research questions and hypotheses, not established discoveries.
Never fabricate literature references, experimental data, benchmark outcomes, model performance, or novelty claims.
Use language such as "to the best of our documented literature search" where appropriate.
Distinguish a software capability, a hypothesis, an experimental observation, and a statistically supported conclusion.
15. Required Completion Report
After creating or updating AGENTS.md:
•	Report the exact path.
•	Summarize its major sections.
•	List any conflicts discovered in existing repository instructions.
•	Confirm whether the file is consistent with the current docs/PLAN.md and docs/TEAM_WORKFLOW.md, if available.
•	Identify any unresolved conflicts instead of silently choosing incompatible rules.
•	Run a basic Markdown or file-integrity check if available.
Acceptance Criteria
This task is complete only when:
1.	AGENTS.md exists at the repository root.
2.	The permanent rules are explicit, actionable, and internally consistent.
3.	The LLM boundary and provider modes are unambiguous.
4.	V0–V3 have exactly one authoritative definition.
5.	Hidden tests are explicitly protected.
6.	Deployment and rollback cannot destructively overwrite unrelated work.
7.	Rule-based risk is not misrepresented as calibrated probability.
8.	The file preserves compatible existing instructions.
9.	No unrelated source code or user changes were overwritten.
10.	The completion report accurately describes verification performed.
Do not proceed to implement other modules as part of this task.
