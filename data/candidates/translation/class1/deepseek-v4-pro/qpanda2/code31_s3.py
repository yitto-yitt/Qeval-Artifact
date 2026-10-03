# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
from pyqpanda import *

def sampler_qiskit() -> Dict[str, float]:
    init_qvm()
    set_random_seed(42)

    q = qAlloc_many(2)
    c = cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)

    shots = 1024
    counts = run_with_configuration(prog, c, shots)

    finalize()

    return {key: value / shots for key, value in counts.items()}
