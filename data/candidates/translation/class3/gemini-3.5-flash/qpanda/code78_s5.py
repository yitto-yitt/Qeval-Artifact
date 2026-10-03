# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def qft_no_swaps(num_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for i in range(num_qubits):
        for j in range(i):
            circuit << CU1(q[j], q[i], -2 * np.pi / (2 ** (i - j + 1)))
        circuit << H(q[i])
    return circuit
