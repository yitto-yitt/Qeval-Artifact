# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import *
import numpy as np

def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)

    state = np.asarray(desired_vector, dtype=np.complex128)
    norm = np.linalg.norm(state)
    if norm == 0:
        qvm.finalize()
        return {"000": 1.0}
    state = state / norm

    prog = QProg()
    prog << amplitude_encode(q, state.tolist())
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1]) << Measure(q[2], c[2])

    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)

    qvm.finalize()

    total = sum(counts.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in counts.items()}
