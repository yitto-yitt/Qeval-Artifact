# EVAL_META: task_id=77, framework=qpanda, class=1
import math

from pyqpanda3.core import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        complex(math.sqrt(probability_dist.get(i, 0)))
        for i in range(2 ** num_qubits)
    ]

    qc = QuantumCircuit(num_qubits)
    qc.initialize(amplitudes, list(range(num_qubits)))
    return qc
