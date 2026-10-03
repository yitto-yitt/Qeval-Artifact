# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import math
machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(10)
def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    q = qubits[:num_qubits]
    for target in range(num_qubits - 1, -1, -1):
        for control in range(num_qubits - 1, target, -1):
            angle = -math.pi / (2 ** (control - target))
            circuit << CR(angle, q[control], q[target])
        circuit << H(q[target])
    return circuit
machine.finalize()
