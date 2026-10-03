# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qalloc, H, CP
from math import pi

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qubits = qalloc(num_qubits)
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            angle = -pi / (2 ** (k - j))
            circuit << CP(qubits[k], qubits[j], angle)
        circuit << H(qubits[j])
    return circuit
