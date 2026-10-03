# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
from pyqpanda import QCircuit, Qubit, amplitude_encode

def circuit_from_probability_dist(probability_dist):
    max_key = max(probability_dist.keys())
    num_qubits = math.ceil(math.log2(max_key + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
    qubits = [Qubit(i) for i in range(num_qubits)]
    return amplitude_encode(qubits, amplitudes)
