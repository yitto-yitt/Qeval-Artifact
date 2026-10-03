# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda import *


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    circuit = QCircuit()
    circuit.insert(initialize_qstate(qubits, amplitudes))
    return circuit
