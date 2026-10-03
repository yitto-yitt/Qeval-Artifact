# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import *


def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()

    for init_name in ("init_qvm", "init", "initQVM"):
        init_method = getattr(qvm, init_name, None)
        if callable(init_method):
            try:
                init_method()
                break
            except Exception:
                pass

    qalloc = getattr(qvm, "qAlloc_many", None) or getattr(qvm, "qalloc_many", None)
    calloc = getattr(qvm, "cAlloc_many", None) or getattr(qvm, "calloc_many", None)

    q = qalloc(n + 1)
    c = calloc(n)

    prog = QProg()
    ancilla = n

    prog << X(q[ancilla])
    for i in range(n + 1):
        prog << H(q[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[ancilla])

    for i in range(n):
        prog << H(q[i])

    for i in range(n):
        prog << Measure(q[n - 1 - i], c[i])

    run_method = getattr(qvm, "run_with_configuration", None) or getattr(qvm, "runWithConfiguration", None)
    if run_method is None:
        raise AttributeError("No run_with_configuration method available in pyqpanda3 CPUQVM")

    try:
        result = run_method(prog, c, 1)
    except TypeError:
        result = run_method(prog, 1, c)

    counts = result
    if hasattr(result, "get_counts") and callable(result.get_counts):
        counts = result.get_counts()

    def normalize_key(key):
        if isinstance(key, bytes):
            key = key.decode()
        elif isinstance(key, int):
            key = format(key, "0{}b".format(n))
        else:
            key = str(key)
        key = key.replace(" ", "")
        if n == 0:
            return ""
        if len(key) < n and all(ch in "01" for ch in key):
            key = key.zfill(n)
        return key

    bitstrings = []
    if isinstance(counts, dict):
        for key, value in counts.items():
            try:
                count = int(value)
            except Exception:
                try:
                    count = 1 if float(value) > 0 else 0
                except Exception:
                    count = 1
            for _ in range(max(count, 0)):
                bitstrings.append(normalize_key(key))
        if not bitstrings and counts:
            best_key = max(counts, key=counts.get)
            bitstrings = [normalize_key(best_key)]
    elif isinstance(counts, (list, tuple)):
        bitstrings = [normalize_key(x) for x in counts]
    else:
        bitstrings = [normalize_key(counts)] if n > 0 else [""]

    if not bitstrings:
        bitstrings = [""]

    return [bitstrings, result]
