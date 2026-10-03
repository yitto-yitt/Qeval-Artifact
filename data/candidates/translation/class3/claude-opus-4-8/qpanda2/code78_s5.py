# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)

def qft_no_swaps(num_qubits):
    prog = pq.QCircuit()
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            angle = -np.pi / (2 ** (k - j))
            prog << pq.CR(qubits[k], qubits[j], angle)
        prog << pq.H(qubits[j])
    return prog

machine.finalize()
