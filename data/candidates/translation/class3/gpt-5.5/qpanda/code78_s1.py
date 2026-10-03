# EVAL_META: task_id=78, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, CP

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for target in range(num_qubits):
        for control in range(target - 1, -1, -1):
            circuit << CP(control, target, -pi / (2 ** (target - control)))
        circuit << H(target)
    return circuit
