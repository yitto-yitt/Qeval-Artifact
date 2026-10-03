# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda3.core import QCircuit, qAlloc, amplitude_encode

def circuit_from_probability_dist(probability_dist):
    max_key = max(probability_dist.keys())
    num_qubits = math.ceil(math.log2(max_key + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
    
    qubits = [qAlloc() for _ in range(num_qubits)]
    circuit = QCircuit()
    circuit << amplitude_encode(qubits, amplitudes)
    return circuit
