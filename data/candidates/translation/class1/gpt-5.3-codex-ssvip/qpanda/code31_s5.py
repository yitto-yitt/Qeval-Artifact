# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import *

def sampler_qiskit() -> Dict[str, float]:
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    machine.finalize_qvm()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
