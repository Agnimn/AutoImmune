\# Phase 6 — LLM Pilot Notes



\## 1. Scope



This document records observed Phase 6 pilot results for faults F01, F04, and F06. Results are limited to the recorded runs and current artifacts. They are not general accuracy or safety claims.



\## 2. Environment



\- Model: `qwen2.5-coder:7b`

\- Endpoint: `http://localhost:11434/v1`

\- Python: 3.12.6

\- Test suite: 170 passed, 0 failed, 0 skipped in 768.14 seconds.

\- Analysis command: `.\\.venv\\Scripts\\python.exe analyse.py`

\- Full test command: `.\\.venv\\Scripts\\python.exe -m pytest`



No API keys are recorded in this document.



\## 3. Live diagnosis and patch drafting



The recorded live diagnosis and patch experiments cover F01, F04, and F06. The pilot report records 25 LLM candidate units, all unlabelled.



\- Live patch drafting: 0 of 9 patches applied. The observed issue was that generated diffs lacked the `---` and `+++` file headers required by the patch application workflow.

\- F01 localisation: 8/8 top-1 and 8/8 top-3 hits in the current analysis report.

\- F04 localisation: 0/8 top-1 and 0/8 top-3 hits in the current analysis report. This is a concerning result for this pilot and requires investigation.

\- F06 localisation: 9/9 top-1 and 9/9 top-3 hits in the current analysis report.



These counts are observations from the current pilot artifacts only. The samples are not independent fault cases, and draft labels have not been reviewed for publication-quality claims.



\## 4. F06 run evidence



\### `f06-live-1`



\- Diagnosis mode: live

\- Patch mode: live

\- Diagnosis samples in run metadata: 1

\- Gate-only run: true



\### `f06-live-diag-1` through `f06-live-diag-4`



\- Diagnosis mode: live

\- Patch mode: scripted

\- Run-level diagnosis sample count: 3 for runs 1–4

\- Runs 2 and 3 failed during baseline Docker image construction.

\- Run 4 produced the expected run artifacts.



For `f06-live-diag-4`, the diagnosis artifact records:

\- Model: `qwen2.5-coder:7b`

\- Provider mode: live

\- Three samples, with no disagreement

\- Top-1 hit: true

\- Top-3 hit: true

\- Oracle localisation: false

\- Three recorded successful request attempts



The run metadata's `diag\_samples` field differs from the nested configuration's `diag\_samples` value. This discrepancy should remain visible until its meaning is confirmed.



\### F06 candidate `F06-scripted-05420f6c`



The analysis report records V2 as `error`. The earlier handoff identifies this as a Docker unexpected-EOF/tool error. This is not a successful gate result and must not be presented as a pass.



\## 5. Replay verification



\### `F06-replay-1`



Command:



`.\\.venv\\Scripts\\python.exe -m pipeline run --fault F06 --diag-mode replay --patch-mode replay --gates-only --run-id F06-replay-1`



Outcome: incomplete.



\- Baseline and faulty deployment artifacts were produced.

\- An incident artifact was produced.

\- Step 4, diagnosis and patch replay, stopped with `ProviderError`.

\- Missing cache entry: `94f9106c7dc60f5304fe2548e61ebd10f1e9edec2c4436f6f9829b0010d8bfa3.json`

\- Requested provider: `http://localhost:11434/v1`

\- Model: `qwen2.5-coder:7b`

\- Temperature: `0.2`

\- Diagnosis and patch artifacts were not produced for this replay run.

\- The baseline was restored after the failure.



The cache key depends on the exact prompt, model/provider configuration, temperature, and sample index. Existing cache entries with matching provider/model values do not establish that the required key exists.



Per the replay workflow, do not restart Ollama or generate cache entries to force replay to succeed. F06 replay remains incomplete until a safe, evidence-backed resolution is approved.



F01 and F04 replay have not yet been verified in this work session.



\## 6. Analysis report and labels



The current analysis outputs are:

\- `results/llm\_units.csv`

\- `results/llm\_diagnosis.csv`

\- `results/pilot\_report.md`



The report keeps LLM results separate from scripted candidate metrics. It records 25 units, zero labelled units, and zero human approvals. Policy rates based on labels therefore have no labelled denominator and cannot support safety claims.



The `llm\_diagnosis.csv` header was corrected to use unique denominator names:

\- `top1\_n`

\- `top3\_n`



The regenerated CSV imports successfully and contains three diagnosis rows. `llm\_units.csv` still contains 25 rows.



\## 7. Verification after the analysis change



Full test suite:



`.\\.venv\\Scripts\\python.exe -m pytest`



Result: \*\*170 passed, 0 failed, 0 skipped in 768.14 seconds (12m 48s).\*\*



\## 8. Outstanding items



1\. Determine a safe, approved way to verify replay cache coverage; do not bypass a cache miss.

2\. Verify F01 and F04 replay if suitable existing cache entries are available. Stop and report any cache miss.

3\. Investigate the F04 localisation failure.

4\. Resolve the F06 run-metadata/configuration sample-count discrepancy.

5\. Preserve separation between live LLM and scripted results.

6\. Keep labels as drafts until the required two-person review is complete.

7\. Do not publish general accuracy or safety claims from this small, unlabelled pilot.



\## 9. Evidence limitations



This document records observed artifacts and command outputs. A successful test suite does not prove replay success, patch quality, or production safety. Infrastructure errors and missing artifacts are recorded as blockers rather than passes.



