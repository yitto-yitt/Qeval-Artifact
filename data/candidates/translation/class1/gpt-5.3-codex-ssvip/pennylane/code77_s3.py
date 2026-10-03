# EVAL_META: task_id=77, framework=pennylane, class=1
import math
import pennylane as qml
from pennylane import numpy as np


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    amplitudes = np.array(amplitudes, dtype=float)
    norm = np.linalg.norm(amplitudes)
    if norm == 0:
        amplitudes = np.zeros_like(amplitudes)
        amplitudes[0] = 1.0
    else:
        amplitudes = amplitudes / norm

    def circuit():
        qml.StatePrep(amplitudes, wires=range(num_qubits))

    return qml.tape.QuantumTape.from_queue(qml.queuing.AnnotatedQueue(), circuit)
