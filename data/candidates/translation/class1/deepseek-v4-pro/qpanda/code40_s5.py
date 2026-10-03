# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import *

def init_random_3qubit(desired_vector):
    init()
    q = qalloc(3)
    c = cbits(3)

    vec = np.array(desired_vector, dtype=complex)
    vec = vec / np.linalg.norm(vec)

    n = len(vec)
    A = np.eye(n, dtype=complex)
    A[:, 0] = vec
    unitary, _ = np.linalg.qr(A)

    gate = QGate(unitary)
    prog = QProg()
    prog << gate(q[0], q[1], q[2])
    prog << measure_all(q, c)

    counts = run_with_configuration(prog, c, 100000)
    total = sum(counts.values())
    result = {key: value / total for key, value in counts.items()}

    destroy_quantum_machine()
    return result
