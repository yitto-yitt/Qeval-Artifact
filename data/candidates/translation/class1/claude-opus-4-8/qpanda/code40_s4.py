# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import QCircuit, QProg, QGate, CPUQVM

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    norm = np.linalg.norm(vec)
    if norm != 0:
        vec = vec / norm

    n = 3
    circ = QCircuit(n)
    gate = QGate(list(range(n)), vec)
    circ << gate

    prog = QProg()
    prog << circ
    prog.measure_all()

    qvm = CPUQVM()
    qvm.run(prog, 4096)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
