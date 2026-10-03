# EVAL_META: task_id=77, framework=cirq, class=1
import math
import numpy as np
import cirq


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2 ** num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    amplitudes = np.array(amplitudes, dtype=complex)
    norm = np.linalg.norm(amplitudes)
    if norm > 0:
        amplitudes = amplitudes / norm

    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.StatePreparationChannel(amplitudes)
    circuit = cirq.Circuit()
    circuit.append(gate.on(*qubits))
    return circuit
