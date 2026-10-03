# EVAL_META: task_id=78, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, U1, CNOT


def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for target in range(num_qubits):
        for control in range(target):
            angle = -pi / (2 ** (target - control))
            circuit << U1(control, angle / 2)
            circuit << U1(target, angle / 2)
            circuit << CNOT(control, target)
            circuit << U1(target, -angle / 2)
            circuit << CNOT(control, target)
        circuit << H(target)
    return circuit
