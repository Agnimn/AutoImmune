This document prevents the three team members from overwriting each other's modules, breaking shared interfaces, or merging untested code.
TASK: Create the AutoImmune Shared-Repository Team Workflow
Act as a senior engineering team lead, Git workflow architect, integration engineer, and research project coordinator.
Create or carefully update docs/TEAM_WORKFLOW.md in the AutoImmune repository.
This file must establish a practical, enforceable collaboration process for three team members sharing one Git repository and developing interdependent components of the AutoImmune self-healing software research project.
Inspect the existing repository and existing project documents before editing. Preserve working code and compatible conventions. Do not implement the application itself as part of this task.
The resulting workflow must minimize merge conflicts, prevent accidental loss of work, keep interface contracts stable, and ensure that every merged module can be integrated and demonstrated.
1. Project and Team Context
AutoImmune contains:
•	A Python orchestration pipeline.
•	An initial Java 17/Spring Boot target application.
•	Controlled source-level fault fixtures.
•	A provider abstraction supporting live, replay, scripted, and rule-based modes.
•	An isolated Docker validation sandbox.
•	A deterministic decision engine.
•	Deployment, recovery, and rollback components.
•	Evidence recording and experimental analysis.
Three members will collaborate on one shared repository.
The repository must have one authoritative architecture in docs/PLAN.md and permanent operating rules in AGENTS.md.
Team members must not independently redefine architecture, validation gates, decision rules, or telemetry schemas.
2. Ownership and Responsibility Matrix
Use the following initial ownership allocation unless existing team agreements explicitly specify otherwise.
Member	Primary ownership	Responsibilities
Member 1	app/, faults/, pipeline/observe.py, pipeline/detector.py	Target application, baseline behaviour, reproducible faults, visible reproduction tests, permitted hidden-test fixtures, detection rules, incident schema integration.
Member 2	pipeline/llm_provider.py, pipeline/diagnose.py, pipeline/patch_generator.py, pipeline/sandbox.py, pipeline/decide.py, config/decision.yaml	Provider abstraction, structured diagnosis, candidate diff handling, isolated validation, validation result parsing, deterministic decision policy.
Member 3	pipeline/deploy.py, pipeline/rollback.py, pipeline/record.py, analyse.py	Staged deployment, health monitoring, rollback, evidence persistence, dataset evaluation, statistical reports and reproducibility.
These are primary ownership boundaries, not permission to ignore dependencies.
Shared contracts, AGENTS.md, docs/PLAN.md, docs/TEAM_WORKFLOW.md, build configuration, and cross-cutting security changes require coordinated review.
If the actual repository uses different module names, map responsibilities to the existing modules instead of creating duplicate files.
3. Explicit Ownership Rules
Each module must have one primary owner.
The owner is responsible for:
•	Implementation.
•	Unit tests.
•	Documentation of module inputs and outputs.
•	Error handling.
•	Acceptance checks.
•	Reviewing changes that directly affect the module.
•	Providing a reproducible integration example.
•	Fixing defects found during integration.
Other members may propose changes but must coordinate with the owner before modifying the same module.
No member may silently overwrite, replace, or remove another member's implementation.
If an urgent cross-module fix is needed, notify the owner, make the smallest compatible change, and document the handoff.
Ownership does not mean that a module is exempt from peer review.
4. Repository Setup and Branching Strategy
The repository should have one shared main branch containing the latest integrated, reviewed, working baseline.
Use these feature branches as initial conventions:
•	Member 1: feat/target-app-detector
•	Member 2: feat/providers-sandbox-decide
•	Member 3: feat/deploy-record-analyse
Bug fixes should use descriptive names such as fix/sandbox-timeout or fix/rollback-state.
Documentation-only changes may use docs/architecture-contracts.
Do not assume a branch exists or create duplicate branches without checking the repository.
Initial Setup Sequence
1.	Inspect the existing Git repository and current branch.
2.	Preserve existing local changes.
3.	Confirm the authoritative root AGENTS.md.
4.	Confirm docs/PLAN.md and this workflow document exist.
5.	Agree on module ownership and shared interface contracts.
6.	Create or confirm the feature branches.
7.	Ensure each member starts from a documented baseline commit.
Do not reset, force-push, rewrite shared history, or discard uncommitted changes without explicit team authorization.
5. Dependency-Aware Integration Order
The preferred integration order is:
1.	Member 1: Deliver the target application, known-good baseline, source-level fault fixtures, visible tests, and incident-detection contract.
2.	Member 2: Integrate against that baseline and deliver provider, diagnosis, patch handling, sandbox validation, and decision logic.
3.	Member 3: Integrate against the established decision and evidence contracts, then deliver deployment, rollback, recording, and analysis.
4.	All members: Run the full integration suite, verify acceptance checks, resolve interface mismatches, and prepare the demo.
This is the preferred order, not a reason to block independent work.
Members may develop using agreed interface stubs or fixtures before upstream modules are merged. Those stubs must be clearly labelled as test fixtures and replaced or verified during integration.
After an upstream module changes its public contract, downstream owners must rebase or merge the agreed change and rerun the affected tests.
6. Git Commit and Pull Request Protocol
Use small, meaningful commits.
Each commit should address one coherent change, such as:
•	Add target reproduction tests.
•	Implement detector threshold configuration.
•	Add provider response schema validation.
•	Implement V2 regression gate.
•	Add decision-policy unit tests.
•	Add staged rollback verification.
•	Add evidence aggregation metrics.
Before opening a pull request:
1.	Fetch the latest shared branch.
2.	Integrate the latest compatible changes.
3.	Inspect the complete diff.
4.	Confirm that unrelated changes are not included.
5.	Run the relevant unit tests.
6.	Run the module's acceptance checks.
7.	Run relevant integration tests.
8.	Update documentation and schemas where needed.
9.	Record any known limitation or unexecuted test.
Every pull request must include:
•	Purpose and scope.
•	Files changed.
•	Interfaces affected.
•	Tests executed and actual results.
•	Acceptance checks passed or failed.
•	Security and rollback implications where applicable.
•	Follow-up work and known limitations.
Do not report tests as passing if they were not run.
Require at least one other team member to review changes affecting shared interfaces, security controls, validation policy, deployment, rollback, or evidence integrity.
7. Shared Interface Contracts
The following artifacts are shared contracts:
•	incident.json
•	diagnosis.json
•	Candidate patch metadata.
•	gates.json
•	decision.json
•	Deployment and rollback records.
•	evidence.jsonl
Each contract must have:
•	A documented schema.
•	Required and optional fields.
•	Defined field types.
•	Explicit failure and missing-data semantics.
•	A schema version.
•	Representative valid and invalid test fixtures.
Before changing a contract:
1.	Identify every producer and consumer.
2.	Propose the change in the relevant pull request.
3.	Obtain agreement from affected module owners.
4.	Update the schema and docs/PLAN.md.
5.	Update producer and consumer code.
6.	Add compatibility or migration tests.
7.	Verify the full integration path.
Do not rename a field or change its meaning silently.
Prefer additive, backward-compatible changes where practical. If compatibility cannot be maintained, document the breaking change and update all dependent modules in the same coordinated integration effort.
8. Provider and Candidate Handling Rules
Member 2 owns the provider and candidate-generation interfaces.
All provider responses must declare their source mode:
•	live
•	replay
•	scripted
•	rule
Record diagnosis and patch-generation modes separately when necessary.
Never combine scripted and live-LLM outcomes in an evaluation table without explicitly separating them.
Replay caches must use a documented schema and stable identifiers. Cache files must not contain secrets, private credentials, or unapproved sensitive source material.
Every candidate must have a stable candidate_id, source-mode metadata, patch reference, and validation status.
Candidate-generation failure must be recorded explicitly. Do not create a fake successful candidate to satisfy a test.
All generated diffs must be validated before being passed to the sandbox.
9. Validation Gate Ownership and Consistency
Use the canonical definitions in docs/PLAN.md:
•	V0: patch integrity and compilation.
•	V1: visible target reproduction tests.
•	V2: existing regression tests.
•	V3: static analysis and security checks.
Runtime replay and deployment health checks are separate runtime validation stages.
Member 2 owns the sandbox and validation-gate implementation. Member 1 owns the target's intended behaviour and visible reproduction tests. Member 3 owns post-deployment health monitoring and recovery outcomes.
No member may change a gate definition independently.
If a tool is missing, a process times out, or validation cannot complete, record the actual status. Never turn an error into a pass merely to satisfy an acceptance check.
Hidden ground-truth tests must never be included in candidate sandbox mounts or made available to diagnosis and patch-generation providers.
10. Security and Destructive Operation Rules
All members must comply with AGENTS.md.
Never:
•	Execute candidate source code directly on the host as part of validation.
•	Mount the Docker socket inside the candidate container.
•	Expose hidden tests or ground-truth labels to the candidate.
•	Place secrets in source control or replay fixtures.
•	Disable required security checks to obtain a green build.
•	Run destructive Git commands against another member's working tree.
•	Use git checkout . as a general rollback strategy.
•	Automatically deploy an escalated candidate without explicit approval.
•	Bypass mandatory validation because a demo is approaching.
The deployment owner must retain a known-good deployment artifact and verify rollback behaviour.
Security-sensitive changes require explicit peer review and relevant tests.
11. Testing Responsibilities
Member 1
Must verify:
•	The known-good target application builds.
•	Each source-level fault can be reproduced.
•	Visible target tests behave as documented.
•	Healthy operation does not trigger false incidents under the specified test conditions.
•	Fault metadata matches the actual fixtures.
Member 2
Must verify:
•	Provider modes are explicitly identified.
•	Offline scripted/replay execution works without API credentials.
•	Invalid model responses and invalid diffs fail safely.
•	V0–V3 run in the sandbox.
•	Sandbox network isolation is actually tested.
•	Hidden tests are not mounted.
•	Every decision-policy branch has unit tests.
Member 3
Must verify:
•	Deployment is limited to eligible or explicitly approved candidates.
•	Health checks have bounded timeouts.
•	Healthy deployments are promoted.
•	Controlled unhealthy deployments trigger rollback.
•	Rollback does not destroy unrelated working-tree changes.
•	Evidence records are valid and complete.
•	Analysis reports can be regenerated from saved evidence.
Full-Team Integration
Before a demonstration or release, verify:
•	The documented CLI entry point works.
•	At least three distinct controlled faults run through the intended pipeline.
•	Human approval works for an escalated candidate.
•	At least one valid repair can reach the eligible deployment path.
•	A controlled post-deployment failure demonstrates rollback.
•	Evidence and reports reflect actual execution results.
12. Continuous Integration and Local Verification
Use the existing CI system if available. Otherwise, document a minimal local verification process.
At minimum, the project should provide commands for:
•	Python unit tests.
•	Target application build and tests.
•	Schema and contract validation.
•	Decision-policy tests.
•	Sandbox isolation tests.
•	Integration tests.
•	Evidence integrity checks.
•	Markdown or documentation checks where practical.
Keep the build and test commands documented in the repository's README or development guide.
Use pinned or documented tool versions where practical.
Do not make external network access a hidden requirement for replay-mode testing.
13. Evidence Integrity and Research Reproducibility
All team members must preserve the distinction between:
•	Provider output.
•	Candidate validation evidence.
•	Decision-time information.
•	Deployment outcome.
•	Post-hoc ground-truth labels.
Ground-truth labels must not leak into the model input or decision engine.
Never manually edit results to make a baseline appear better or worse.
Do not fabricate timings, repair success rates, calibration values, or unsafe deployment counts.
Record failed runs and exclusions with reasons. Use reproducible configuration files and stable fault/candidate identifiers.
Member 3 is responsible for the evidence aggregation and analysis implementation, but every member must provide complete and accurate module telemetry.
14. Team Communication and Handoffs
For every module handoff, the owner must provide:
1.	Module purpose.
2.	Public inputs and outputs.
3.	Required configuration.
4.	Commands to run it.
5.	Tests and acceptance checks.
6.	Example valid artifacts.
7.	Known limitations.
8.	Current branch and relevant commit identifier.
For a blocking issue, provide:
•	The exact failure.
•	Reproduction steps.
•	Relevant log or test output.
•	Expected behaviour.
•	Actual behaviour.
•	The responsible module owner.
•	The proposed next step.
Do not send vague messages such as "it doesn't work" without reproducible evidence where practical.
Resolve disagreements about architecture through docs/PLAN.md and explicit team agreement, not through incompatible implementations in separate modules.
15. Change Management
Any change affecting architecture, validation gates, risk policy, provider modes, telemetry contracts, security controls, or deployment semantics must trigger a documentation review.
The responsible member must update docs/PLAN.md and the relevant tests as part of the same coordinated change.
If a requirement is uncertain, record an open question rather than allowing three independent interpretations.
When a new implementation makes an existing document inaccurate, update the documentation. Do not leave contradictory descriptions in the repository.
16. Completion and Release Checklist
Before declaring the integrated prototype ready:
•	All three members' deliverables are merged into the shared integration branch.
•	No unrelated local changes were overwritten.
•	Public contracts match their documented schemas.
•	Provider-mode labels are accurate.
•	V0–V3 use the authoritative definitions.
•	Hidden tests remain isolated.
•	Decision branches are covered by tests.
•	Deployment approval rules are enforced.
•	Rollback restores the known-good deployment state.
•	Evidence records are traceable and valid.
•	Analysis reports are generated from actual recorded data.
•	Demonstration commands and prerequisites are documented.
•	Known limitations and unverified checks are disclosed.
A release must not be described as complete merely because the application starts or the dashboard renders.
17. Required Completion Report
After creating or updating docs/TEAM_WORKFLOW.md:
•	Confirm the exact path.
•	Summarize the ownership and integration rules.
•	Identify conflicts with the current repository or project plan.
•	Confirm the canonical contract and gate definitions.
•	State which Markdown or integrity checks were actually executed.
•	List unresolved questions requiring team agreement.
Acceptance Criteria
The task is complete only when:
1.	docs/TEAM_WORKFLOW.md exists at the correct path.
2.	All three members have clear primary responsibilities.
3.	The dependency-aware integration order is documented.
4.	Branching, pull requests, and verification requirements are explicit.
5.	Shared contracts cannot be changed silently.
6.	Provider modes and hidden-test isolation are documented.
7.	Rollback and destructive Git operations are addressed.
8.	Research data integrity and reproducibility rules are explicit.
9.	The workflow agrees with AGENTS.md and docs/PLAN.md.
10.	The completion report accurately states what was verified.
Do not implement the application as part of this task.

