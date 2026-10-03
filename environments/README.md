# Environment Notes

The artifact does not pin package versions in this snapshot. Install the
dependencies required by the evaluation setting you intend to run, then record
the exact environment with:

```powershell
python -m pip freeze > environments/installed-versions.txt
```

The dependency files are grouped by evaluation scope:

- `requirements-base.txt`: input validation and result aggregation only.
- `requirements-direct.txt`: direct Qiskit evaluation.
- `requirements-translation-main.txt`: cross-framework evaluation for Cirq,
  PennyLane, and QPanda3.
- `requirements-translation-qpanda2.txt`: supplementary QPanda2 evaluation.
- `requirements-zx.txt`: ZX full-reduce verification.

Install examples:

```powershell
python -m pip install -r environments/requirements-direct.txt
python -m pip install -r environments/requirements-translation-main.txt
python -m pip install -r environments/requirements-zx.txt
```

Candidate programs are executable Python code. Use a disposable environment
without personal files, credentials, or unnecessary network access before
running commands that pass `--execute-candidates`.
