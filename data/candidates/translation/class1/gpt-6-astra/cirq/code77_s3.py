# EVAL_META: task_id=77, framework=cirq, class=1
import math

import cirq
import numpy as np


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = np.array(
        [
            math.sqrt(probability_dist.get(basis_state, 0))
            for basis_state in range(2**num_qubits)
        ],
        dtype=np.complex128,
    )
    if not np.isclose(np.linalg.norm(amplitudes), 1.0):
        raise ValueError("Probabilities must sum to 1.")

    qubits = cirq.LineQubit.range(num_qubits)
    return cirq.Circuit(cirq.StatePreparationChannel(amplitudes).on(*qubits))
