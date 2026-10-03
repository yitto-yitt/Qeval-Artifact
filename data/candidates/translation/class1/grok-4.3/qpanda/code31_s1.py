# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def sampler_qiskit() -> Dict[str, float]:
    qvm = CPUQVM()
    qvm.initQVM()
    qvm.set_random_seed(42)
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)
    total = sum(counts.values())
    return {key: val / total for key, val in counts.items()}
