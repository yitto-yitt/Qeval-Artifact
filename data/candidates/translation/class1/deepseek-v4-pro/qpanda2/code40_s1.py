# EVAL_META: task_id=40, framework=qpanda2, class=1
from pyqpanda import *
import numpy as np
import builtins

def init_random_3qubit(desired_vector):
    shots = 1024
    init_qvm()
    q = qAlloc_many(3)
    c = cAlloc_many(3)
    prog = QProg()
    data = np.abs(np.asarray(desired_vector)).astype(float)
    norm = np.linalg.norm(data)
    if norm > 1e-12:
        data = data / norm
    else:
        data = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    data = data.tolist()
    prog << amplitude_encode(q, data)
    for i in range(3):
        prog << measure(q[i], c[i])
    result = run_with_configuration(prog, c, shots)
    finalize_qvm()
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
