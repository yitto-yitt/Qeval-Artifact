# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CR


def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for j in range(num_qubits):
        target = num_qubits - 1 - j
        for k in range(target + 1, num_qubits):
            angle = -3.141592653589793 / (2 ** (k - target))
            circuit << CR(target, k, angle)
        circuit << H(target)
    return circuit
