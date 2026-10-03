# EVAL_META: task_id=65, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, H, U1, SWAP

def QFT(n):
    circuit = QProg()
    for target in range(n - 1, -1, -1):
        circuit << H(target)
        for control in range(target):
            angle = pi / (2 ** (target - control))
            circuit << U1(target, angle).control([control])
    for qubit in range(n // 2):
        circuit << SWAP(qubit, n - qubit - 1)
    return circuit
