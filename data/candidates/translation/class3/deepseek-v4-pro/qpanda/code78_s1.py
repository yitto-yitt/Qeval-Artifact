# EVAL_META: task_id=78, framework=qpanda, class=3
import math
from pyqpanda3.core import QuantumMachine, QProg, H, CP

def qft_no_swaps(num_qubits):
    machine = QuantumMachine()
    qubits = machine.qAllocMany(num_qubits)
    prog = QProg()
    for i in range(num_qubits - 1, -1, -1):
        prog << H(qubits[i])
        for j in range(i + 1, num_qubits):
            angle = -2 * math.pi / (2 ** (j - i + 1))
            prog << CP(qubits[j], qubits[i], angle)
    return prog
