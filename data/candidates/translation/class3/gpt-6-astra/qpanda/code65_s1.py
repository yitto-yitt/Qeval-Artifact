# EVAL_META: task_id=65, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, H, U3, CNOT, SWAP

def QFT(n):
    circuit = QProg()
    for target in range(n - 1, -1, -1):
        circuit << H(target)
        for control in range(target):
            angle = pi / 2 ** (target - control)
            circuit << U3(control, 0.0, 0.0, angle / 2)
            circuit << U3(target, 0.0, 0.0, angle / 2)
            circuit << CNOT(control, target)
            circuit << U3(target, 0.0, 0.0, -angle / 2)
            circuit << CNOT(control, target)
    for qubit in range(n // 2):
        circuit << SWAP(qubit, n - qubit - 1)
    return circuit
