# AutoImmune — Runbook

> All commands in this file have been executed during Phase 5 on Windows (PowerShell).
> For Linux, replace `.venv\Scripts\python.exe` with `.venv/bin/python` and use forward slashes.

---

## 1. Prerequisites

| Tool | Required version | Check command |
|------|-----------------|---------------|
| Python | 3.12+ | `python --version` |
| Docker Desktop | 24+ | `docker version` |
| Java | 17 (for local Maven runs only — sandbox uses Docker) | `java --version` |
| Git | Any | `git --version` |

Docker images required at runtime (pulled automatically by the test suite if absent):

```
maven:3.9-eclipse-temurin-17   (V0–V2 gate; ~775 MB)
semgrep/semgrep:1.100.0        (V3 gate; ~2.3 GB)
alpine:latest                  (network-isolation test)
```

Maven dependency cache volume (created automatically, speeds up builds):

```
docker volume ls | grep autoimmune-m2
```

---

## 2. Repository setup (clean machine)

```powershell
# Clone and enter the repo
git clone <repo-url> AutoImmune
cd AutoImmune

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt
```

**`requirements.txt` contents:**

```
requests
jsonschema
docker
pyyaml
semver
pytest
pytest-timeout
```

---

## 3. Environment variables (optional — rule/scripted mode needs none)

For live LLM mode only (Phase 6):

```powershell
# Copy the example and fill in values
copy .env.example .env
# Edit .env and set:
#   LLM_BASE_URL=http://localhost:11434/v1   (Ollama) or your hosted endpoint
#   LLM_MODEL=qwen2.5-coder:7b
#   LLM_API_KEY=your-key-or-empty-string
```

For Phase 5 (rule + scripted mode), no `.env` file is needed.

---

## 4. Build the sandbox Docker image

The sandbox image (`order-service`) is built automatically by the test suite and by `python -m pipeline run`.
To pre-build it manually:

```powershell
# Verify the Maven and Semgrep images are present
docker images --format "table {{.Repository}}`t{{.Tag}}`t{{.Size}}"
```

Expected output (images must be present before running tests):

```
REPOSITORY        TAG                      SIZE
maven             3.9-eclipse-temurin-17   775MB
semgrep/semgrep   1.100.0                  2.29GB
alpine            latest                   13MB
```

Pull if missing:

```powershell
docker pull maven:3.9-eclipse-temurin-17
docker pull semgrep/semgrep:1.100.0
docker pull alpine:latest
```

---

## 5. Run the test suite

```powershell
.venv\Scripts\python.exe -m pytest
```

Latest recorded result: **174 passed, 0 failed, 0 skipped**.
This is a recorded result, not a guaranteed count for future runs.
Approximate duration: 13–15 minutes (Docker sandbox tests dominate).

Non-Docker tests only (fast path, ~30 seconds):

```powershell
.venv\Scripts\python.exe -m pytest -m "not docker"
```

Expected: **154 passed, 0 failed, 0 skipped**

---

## 6. Run a single fault (full pipeline)

```powershell
# Rule-based diagnosis + scripted candidates (no LLM needed)
.venv\Scripts\python.exe -m pipeline run --fault F06 --diag-mode rule --patch-mode scripted
.venv\Scripts\python.exe -m pipeline run --fault F01 --diag-mode rule --patch-mode scripted
.venv\Scripts\python.exe -m pipeline run --fault F04 --diag-mode rule --patch-mode scripted
```

The banner printed at the start shows:
```
fault=F06  diag_mode=rule  patch_mode=scripted   (no LLM: rule/scripted results)
```

Outputs under `runs/<run_id>/`:
- `run.json` — parameters
- `baseline.json` — baseline health at start
- `faulty_deploy.json` — faulty build deployment
- `incident.json` — detected incident
- `diagnosis.json` — ranked causes
- `patches.json` — candidate diffs
- `<candidate_id>/decision.json` — gate results + decision
- `summary.json` — final table
- `evidence.jsonl` — run's evidence rows (also appended to `results/evidence.jsonl`)

---

## 7. Gates-only mode (validates gates without deploying)

```powershell
.venv\Scripts\python.exe -m pipeline run --fault F06 --diag-mode rule --patch-mode scripted --gates-only
```

Stops after step 5 (gates + decisions). Still writes evidence rows to `results/evidence.jsonl`.

---

## 8. Approve an ESCALATE candidate (interactive)

When a candidate is ESCALATE, the CLI prompts:

```
Patch: <candidate_id>  Tier: medium  Decision: ESCALATE
Reasons:
  diff changes 25 lines, more than max_diff_lines (20)
Diff:
  <diff content shown here>
Approve? [approve/reject]:
```

Type `approve` or `reject` and press Enter.

To run the F04 correct candidate (which is ESCALATE):

```powershell
.venv\Scripts\python.exe -m pipeline run --fault F04 --diag-mode rule --patch-mode scripted `
    --candidate F04-scripted-4d0272b1
```

---

## 9. Run the staged rollback demo (S3b)

```powershell
# Deploy the slow candidate — passes all gates, then p95 breaches 2 s, automatic rollback
.venv\Scripts\python.exe -m pipeline run --fault F06 --diag-mode rule --patch-mode scripted `
    --candidate F06-scripted-7509cb64
```

Expected outcome: deployed → p95 latency breach → `rolled_back=True` in evidence row → `recovery_s` recorded.

---

## 10. Run a good patch and promote (S3a / good path)

```powershell
# Deploy F06 correct candidate — passes gates, health window OK, promoted
.venv\Scripts\python.exe -m pipeline run --fault F06 --diag-mode rule --patch-mode scripted `
    --candidate F06-scripted-<correct-id>
```

Run `analyse.py` after to confirm the row shows `deployed=true`, `rolled_back=false`.

---

## 11. Regenerate the pilot report

```powershell
.venv\Scripts\python.exe analyse.py
```

Reads `results/evidence.jsonl` and `faults/*/candidates/labels.json`.  
Writes `results/units.csv`, `decisions_by_fault.csv`, `unsafe_first_stop.csv`, `policies.csv`,
`rollbacks.csv`, `approvals.csv`, and `results/pilot_report.md`.

Output is deterministic: same inputs produce byte-identical files.

## 11.1. Regenerate the offline evidence dashboard

Run this command from the repository root in Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe tools\make_dashboard.py
```

The default output is `results/dashboard.html`.

To specify the output path explicitly:

```powershell
.\.venv\Scripts\python.exe tools\make_dashboard.py --out results\dashboard.html
```

The dashboard is a self-contained HTML report generated from repository evidence, analysis outputs, and documentation. Regenerate the analysis report first when the underlying evidence has changed.

---

## 12. Linux equivalents

Replace `.venv\Scripts\python.exe` with `.venv/bin/python`.  
Replace PowerShell backtick `` ` `` for line continuation with `\`.

```bash
.venv/bin/python -m pytest
.venv/bin/python -m pipeline run --fault F06 --diag-mode rule --patch-mode scripted
.venv/bin/python analyse.py
```

---

## 13. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `docker: command not found` | Docker Desktop not in PATH | Start Docker Desktop; verify `docker version` |
| Tests hang >20 min | `autoimmune-m2` volume missing; first Maven download | Let it complete once; subsequent runs use the cache |
| `order-service image not found` | Image not built yet | Run `pytest` once; it builds the image |
| `No incident within 60 s` in pipeline run | App not responding or probe config wrong | Check Docker is running; `docker ps` should show `autoimmune-app` |
| `ProviderError: no cached entry` | Running replay mode without cache entries | Use `--diag-mode rule --patch-mode scripted` for Phase 5 |
| V3 `timeout` | Semgrep image slow to start | Run again; image cold-start on first use |

---

## 14. Demo-day checklist

### Pre-flight (day before)
- [ ] Docker Desktop running and healthy
- [ ] All Docker images present (`docker images`)
- [ ] `autoimmune-m2` volume present (`docker volume ls`)
- [ ] Full test suite passes: run `pytest` and verify 0 failures (historical records: 170 passed Phase 5 baseline; 174 passed recorded with dashboard tests)
- [ ] Rehearsed run saved in `runs/` (at least one F06, F01, F04 run)
- [ ] `analyse.py` produces `results/pilot_report.md` with 16 units

### Day of demo — before the session
- [ ] Docker Desktop started
- [ ] Terminal open in repo root with `.venv` activated
- [ ] Check app is not already running: `docker ps`
- [ ] Run non-Docker tests as a quick sanity check: `pytest -m "not docker" -q`

### Demo steps (plan section 8.2)

1. **Show banner** — `python -m pipeline run --fault F06 --diag-mode rule --patch-mode scripted`
   → Banner shows `fault=F06  diag_mode=rule  patch_mode=scripted  (no LLM: rule/scripted results)`

2. **Detection** — Faulty build deployed; detector raises probe_mismatch incident within 60 s

3. **Diagnosis** — Rule-based: top project frame gives file and line (oracle_localisation=True for rule mode)

4. **Candidates** — 6 scripted candidates listed

5. **Gates** — V0–V3 results shown per candidate; V1/V2/V3 each stop at least one candidate

6. **Decision table** — `print_table()` shows tier, decision, result per candidate

7. **A8 approval** — Run F04 with ESCALATE candidate; type `approve` at the prompt; show it deploys

8. **A9 rollback demo** — Run F06 with slow candidate; show it deploys then rolls back automatically

9. **A10 evidence** — Run `analyse.py`; show `results/pilot_report.md` with 16 units, V1/V2/V3 totals

10. **Summary** — Show `git status --short` (no uncommitted secrets); state Phase 6 deferred items

### Likely questions and answers

| Question | Answer |
|----------|--------|
| "Where is the AI?" | In `providers.py:LiveProvider.diagnose()` and `draft_patches()`. Rule/scripted mode is an honest fallback; the model is not needed for the pipeline to run. |
| "Is this a real deployment?" | Yes: Docker image swap, health window, automatic rollback. `deploy.py` never uses `git reset`. |
| "How do you know the patch is safe?" | Four gates: V0 compile, V1 target test, V2 full suite, V3 Semgrep. Plus scope rules (diff size, file outside diagnosis, sensitive paths). |
| "What does V3 catch?" | New Semgrep findings introduced by the patch vs the unpatched baseline. The insecure candidates (SQL concatenation) all fail V3. |
| "What about live LLM results?" | Deferred to Phase 6. Scripted candidates test the validation pipeline, not the model. Scripted rows are never counted in LLM metrics. |
| "What is n?" | 16 candidate-gate runs across 3 faults (F01, F04, F06). The Wilson intervals show the sample size; no inferential claims made. |
