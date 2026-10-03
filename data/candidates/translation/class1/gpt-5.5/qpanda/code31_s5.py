# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
import pyqpanda3.core as pq


def sampler_qiskit() -> Dict[str, float]:
    qvm = pq.CPUQVM()

    for name in ("init", "init_qvm"):
        if hasattr(qvm, name):
            getattr(qvm, name)()
            break

    for name in ("set_random_seed", "set_seed", "set_rng_seed"):
        if hasattr(qvm, name):
            try:
                getattr(qvm, name)(42)
            except TypeError:
                pass
            break

    qalloc = getattr(qvm, "qalloc_many", None) or getattr(qvm, "qAlloc_many")
    qubits = qalloc(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])

    def normalize(result):
        if hasattr(result, "items"):
            items = result.items()
        else:
            items = result

        probs = {}
        for key, value in items:
            if isinstance(key, int):
                bitstr = format(key, "02b")
            else:
                bitstr = str(key).replace(" ", "")
            probs[bitstr] = float(value)

        total = sum(probs.values())
        if total != 0.0:
            probs = {k: v / total for k, v in probs.items() if v > 1e-12}
        return probs

    for method_name in ("prob_run_dict", "prob_run"):
        if hasattr(qvm, method_name):
            method = getattr(qvm, method_name)
            try:
                return normalize(method(prog, qubits, -1))
            except TypeError:
                return normalize(method(prog, qubits))

    calloc = getattr(qvm, "calloc_many", None) or getattr(qvm, "cAlloc_many")
    cbits = calloc(2)

    if hasattr(pq, "measure_all"):
        prog << pq.measure_all(qubits, cbits)
    else:
        prog << pq.Measure(qubits[0], cbits[0])
        prog << pq.Measure(qubits[1], cbits[1])

    run_method = getattr(qvm, "run_with_configuration")
    try:
        counts = run_method(prog, cbits, 4096)
    except TypeError:
        counts = run_method(prog, 4096, cbits)

    return normalize(counts)
