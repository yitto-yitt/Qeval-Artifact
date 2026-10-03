# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import *
import numpy as np

def init_random_3qubit(desired_vector):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    vec = np.asarray(desired_vector, dtype=np.complex128)
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("desired_vector must be non-zero")
    vec = vec / norm

    prog = QProg()
    prog << amplitude_encode(q, vec.tolist())
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1]) << Measure(q[2], c[2])

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)

    total = sum(counts.values()) if counts else 1
    probs = {k: v / total for k, v in counts.items()}

    machine.finalize()
    return probs
