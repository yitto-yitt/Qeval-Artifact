# EVAL_META: task_id=78, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, CNOT, U1

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for j in range(num_qubits):
        for k in range(j):
            angle = -pi / (2 ** (j - k))
            circuit << U1(j, angle / 2)
            circuit << U1(k, angle / 2)
            circuit << CNOT(j, k)
            circuit << U1(k, -angle / 2)
            circuit << CNOT(j, k)
        circuit << H(j)
    return circuit
