# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
import builtins
import pyqpanda as pq

def sampler_qiskit():
    if hasattr(pq, "set_random_seed"):
        pq.set_random_seed(42)

    qvm = pq.CPUQVM()
    qvm.init_qvm()

    if hasattr(qvm, "set_random_seed"):
        qvm.set_random_seed(42)

    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.Measure(q[0], c[0]))
    prog.insert(pq.Measure(q[1], c[1]))

    shots = 4096
    counts = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())

    qvm.finalize()

    return {key: value / total for key, value in counts.items()}
