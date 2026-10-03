# EVAL_META: task_id=78, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, CR

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for target in range(num_qubits):
        for control in range(target):
            circuit << CR(control, target, -pi / (2 ** (target - control)))
        circuit << H(target)
    return circuit
