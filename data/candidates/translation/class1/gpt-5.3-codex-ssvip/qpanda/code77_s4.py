# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda3.core import *


def circuit_from_probability_dist(probability_dist):
    max_key = max(probability_dist.keys()) if probability_dist else 0
    num_qubits = math.ceil(math.log2(max_key + 1)) or 1

    amplitudes = []
    for basis_state in range(2 ** num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(num_qubits)

    prog = QProg()
    prog << amplitude_encode(q, amplitudes)

    return prog
