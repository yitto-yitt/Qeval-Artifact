# QEval Artifact

This repository contains the offline evaluation artifact for the QEval study.
It starts from fixed candidate programs already stored in `data/candidates/`.
It does not generate candidates, call LLMs, call external APIs, or include
model request logs or credentials.

## Scope

- Retained benchmark tasks: 78 total, with 20 Sampling tasks, 9 State
  Preparation tasks, and 49 Quantum Operation tasks.
- Direct evaluation covers 3,900 Qiskit candidate positions.
- Translation evaluation covers 15,600 candidate positions across Cirq,
  PennyLane, QPanda3, and supplementary QPanda2.
- Candidate filenames are normalized to `code<ID>_s1.py` through
  `code<ID>_s5.py`; reference implementations remain `code<ID>.py`.
- The `qpanda` directory denotes QPanda3. QPanda2 is a supplementary setting
  and should be run and reported separately.
- This artifact does not reproduce the initial 151-task screening, row-level
  classification labels, manual review records, candidate generation, or the
  unfinished taxonomy Skill.

## Data Layout

```text
data/
|-- candidates/
|   |-- direct/classN/<model>/qiskit/code<ID>_sN.py
|   `-- translation/classN/<model>/<framework>/code<ID>_sN.py
|-- references/
|   |-- direct/classN/code<ID>.py
|   `-- translation/classN/code<ID>.py
|-- task_specs/
|   |-- direct/classN.py
|   `-- translation/classN.py
`-- retained_tasks.csv
```

No source files in the original data directory are modified by this artifact.

## Environment

Dependency lists are under `environments/`. They are intentionally not pinned
to invented versions. After creating a clean evaluation environment, install
the dependency group for the setting you want to run and record the actual
resolved versions:

```powershell
python -m pip install -r environments/requirements-direct.txt
python -m pip freeze > environments/installed-versions.txt
```

Use `requirements-translation-main.txt` for Cirq/PennyLane/QPanda3 translation
evaluation, `requirements-translation-qpanda2.txt` for the supplementary
Qpanda2 setting, and `requirements-zx.txt` for ZX verification.

## Input Validation

From Windows PowerShell at the repository root:

```powershell
python scripts/validate_inputs.py
```

The validator checks the retained task manifest, model directories, frameworks,
and all five sample slots. It does not execute candidate code.

## Running Evaluations

Candidate `.py` files are executable code. Run the commands below only in a
disposable environment without personal files, credentials, or unnecessary
network access. The runners require the explicit `--execute-candidates` flag.

Direct Qiskit evaluation:

```powershell
python scripts/run_direct.py --class-id 1 --run-id <RUN_ID> --execute-candidates
python scripts/run_direct.py --class-id 2 --run-id <RUN_ID> --execute-candidates
python scripts/run_direct.py --class-id 3 --run-id <RUN_ID> --execute-candidates
```

Main translation evaluation:

```powershell
python scripts/run_translation.py --class-id 1 --frameworks cirq,pennylane,qpanda --run-id <RUN_ID> --execute-candidates
python scripts/run_translation.py --class-id 2 --frameworks cirq,pennylane,qpanda --run-id <RUN_ID> --execute-candidates
python scripts/run_translation.py --class-id 3 --frameworks cirq,pennylane,qpanda --run-id <RUN_ID> --execute-candidates
```

Supplementary QPanda2 translation evaluation:

```powershell
python scripts/run_translation.py --class-id 1 --frameworks qpanda2 --run-id <RUN_ID>-qpanda2 --execute-candidates
python scripts/run_translation.py --class-id 2 --frameworks qpanda2 --run-id <RUN_ID>-qpanda2 --execute-candidates
python scripts/run_translation.py --class-id 3 --frameworks qpanda2 --run-id <RUN_ID>-qpanda2 --execute-candidates
```

Windows workflow wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_windows_workflow.ps1
powershell -ExecutionPolicy Bypass -File scripts/run_windows_workflow.ps1 -ExecuteCandidates
powershell -ExecutionPolicy Bypass -File scripts/run_windows_workflow.ps1 -ExecuteCandidates -SupplementaryQpanda2
```

Without `-ExecuteCandidates`, the workflow wrapper performs input validation
only and exits.

## Aggregating Results

After all requested class-level runs complete:

```powershell
python scripts/aggregate_results.py --run-id <RUN_ID>
python scripts/aggregate_results.py --run-id <RUN_ID>-qpanda2 --settings translation
```

Class-level outputs are written under:

```text
results/<RUN_ID>/direct/classN/
results/<RUN_ID>/translation/classN/
```

Each class-level result bundle contains:

- `candidate_results.csv`: one row per evaluated candidate sample.
- `candidate_results.jsonl`: JSONL copy of the candidate-level rows.
- `summary.csv`: pass-rate and pass@k summary by setting/model/framework/class.
- `run_manifest.json`: run parameters, runtime platform, and output row counts.

Aggregate outputs are written under `results/<RUN_ID>/aggregate/`:

- `candidate_results_all.csv` and `.jsonl`: all discovered candidate rows.
- `summary_all.csv`: all discovered rows.
- `candidate_results_main.csv` and `summary_main.csv`: excludes QPanda2.
- `candidate_results_qpanda2.csv` and `summary_qpanda2.csv`: QPanda2 only.
- `aggregate_manifest.json`: aggregate inputs and row counts.

## ZX Verification

ZX verification has separate entry points and should write into the same top
level `results/` tree through `--out-root`:

```powershell
python src/qeval/zx/direct/scripts/run_zx_eval.py --dry-run --out-root results/<RUN_ID>/zx_direct
python src/qeval/zx/translation/scripts/run_zx_eval.py --dry-run --out-root results/<RUN_ID>/zx_translation
```

Remove `--dry-run` only inside a disposable evaluation environment.

## Citation and Reuse

Please cite the associated QEval paper. No reuse license is declared in this
artifact snapshot; add a license only after redistribution rights for the code
and data have been confirmed.
