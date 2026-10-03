# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
import builtins
import pyqpanda as pq

def sampler_qiskit():
    if hasattr(pq, "set_random_seed"):
        try:
            pq.set_random_seed(42)
        except Exception:
            pass

    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        if hasattr(qvm, "set_random_seed"):
            try:
                qvm.set_random_seed(42)
            except Exception:
                pass

        q = qvm.qAlloc_many(2)
        c = qvm.cAlloc_many(2)

        prog = pq.QProg()
        prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
        prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])

        shots = 4096
        counts = qvm.run_with_configuration(prog, c, shots)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        qvm.finalize()
