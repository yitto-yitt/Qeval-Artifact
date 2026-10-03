# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import *

def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)

    state = np.asarray(desired_vector, dtype=np.complex128)
    state = state / np.linalg.norm(state)

    prog = QProg()
    prog << amplitude_encode(q, state.tolist())
    prog << measure_all(q, c)

    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)

    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    qvm.finalize()
    return probs
