# EVAL_META: task_id=78, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import CPUQVM, QCircuit, H, CR

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for j in range(num_qubits):
        for k in range(j):
            circuit << CR(q[k], q[j], -math.pi / (2 ** (j - k)))
        circuit << H(q[j])
    return circuit

atexit.register(machine.finalize)
