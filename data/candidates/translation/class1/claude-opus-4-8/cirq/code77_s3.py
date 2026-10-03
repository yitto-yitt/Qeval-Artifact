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

    target_state = np.array(amplitudes, dtype=np.complex64)
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(target_state).on(*qubits))
    return circuit
