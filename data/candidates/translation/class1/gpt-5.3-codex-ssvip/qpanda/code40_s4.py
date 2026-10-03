# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import *
import numpy as np

def init_random_3qubit(desired_vector):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    vec = np.array(desired_vector, dtype=np.complex128)
    norm = np.linalg.norm(vec)
    if norm == 0:
        machine.finalize()
        return {}
    vec = vec / norm

    prog = QProg()
    prog << amplitude_encode(q, vec.tolist())
    prog << measure_all(q, c)

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)

    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()} if total > 0 else {}

    machine.finalize()
    return probs
