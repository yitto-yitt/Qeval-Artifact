# EVAL_META: task_id=78, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, U3, CNOT


def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for j in range(num_qubits):
        for k in range(j):
            angle = -pi / (2 ** (j - k))
            circuit << U3(j, 0.0, 0.0, angle / 2)
            circuit << U3(k, 0.0, 0.0, angle / 2)
            circuit << CNOT(j, k)
            circuit << U3(k, 0.0, 0.0, -angle / 2)
            circuit << CNOT(j, k)
        circuit << H(j)
    return circuit
