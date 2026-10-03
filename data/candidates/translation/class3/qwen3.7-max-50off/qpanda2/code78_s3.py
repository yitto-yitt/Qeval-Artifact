# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(100)

def qft_no_swaps(num_qubits):
    circ = pq.QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            circ << pq.CR(q[k], q[j], -np.pi / (2**(k-j)))
        circ << pq.H(q[j])
    return circ

machine.finalize()
