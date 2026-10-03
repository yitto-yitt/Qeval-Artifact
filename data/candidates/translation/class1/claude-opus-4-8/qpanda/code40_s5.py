# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import QCircuit, QProg, CPUQVM, measure, Encode

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm

    qvm = CPUQVM()
    n = 3

    enc = Encode()
    enc.amplitude_encode(list(range(n)), vec.tolist())
    circ = enc.get_circuit()

    prog = QProg()
    prog.append(circ)
    for q in range(n):
        prog.append(measure(q, q))

    shots = 10000
    counts = qvm.run(prog, shots)

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
