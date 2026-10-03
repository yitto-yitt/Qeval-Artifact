# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import QCircuit, QProg, CPUQVM, measure

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    norm = np.linalg.norm(vec)
    if norm != 0:
        vec = vec / norm

    n = 3
    qvm = CPUQVM()

    circ = QCircuit(n)
    prog = QProg()
    prog << circ

    machine = qvm
    machine.set_state(vec.tolist()) if hasattr(machine, "set_state") else None

    prog2 = QProg()
    for q in range(n):
        prog2 << measure(q, q)

    full = QProg()
    full << circ

    machine.run(full, 1)

    shots = 8192
    machine2 = CPUQVM()
    machine2.set_state(vec.tolist()) if hasattr(machine2, "set_state") else None

    mprog = QProg()
    for q in range(n):
        mprog << measure(q, q)
    machine2.run(mprog, shots)
    counts = machine2.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
