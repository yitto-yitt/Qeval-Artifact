# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
from pyqpanda import *

def init_random_3qubit(desired_vector):
    init(QMachineType.CPU)
    q = qAlloc_many(3)
    c = cAlloc_many(3)

    state = np.array(desired_vector, dtype=complex)
    norm = np.linalg.norm(state)
    if norm > 0:
        state = state / norm
    state = state.tolist()

    prog = QProg()
    prog << init_qubits(q, state)
    prog << measure_all(q, c)

    shots = 10000
    counts = run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
