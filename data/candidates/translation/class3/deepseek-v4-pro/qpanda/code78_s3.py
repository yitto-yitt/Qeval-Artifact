# EVAL_META: task_id=78, framework=qpanda, class=3
import math
from pyqpanda3.core import QuantumCircuit

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            qc.cp(k, j, -math.pi / (2 ** (k - j)))
        qc.h(j)
    return qc
