# EVAL_META: task_id=77, framework=qpanda2, class=1
import math

from pyqpanda import amplitude_encode, qAlloc_many


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(basis_state, 0))
        for basis_state in range(2 ** num_qubits)
    ]

    qubits = qAlloc_many(num_qubits)
    return amplitude_encode(qubits, amplitudes)
