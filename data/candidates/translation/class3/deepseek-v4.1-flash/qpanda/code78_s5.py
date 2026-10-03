# EVAL_META: task_id=78, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, CP


def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            circuit << CP(j, i, -pi / (2 ** (j - i)))
        circuit << H(i)
    return circuit
