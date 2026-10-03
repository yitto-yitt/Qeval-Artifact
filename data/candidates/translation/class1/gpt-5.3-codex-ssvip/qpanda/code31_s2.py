# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import *

def sampler_qiskit():
    set_random_seed(42)
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)
    qvm.finalize()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
