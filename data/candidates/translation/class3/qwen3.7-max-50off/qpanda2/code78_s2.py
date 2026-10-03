# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def qft_no_swaps(num_qubits):
    q = qubits[:num_qubits]
    circ = pq.QCircuit()
    n = num_qubits
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            k = j - i + 1
            angle = -2.0 * np.pi / (2 ** k)
            circ << pq.CR(angle, q[j], q[i])
        circ << pq.H(q[i])
    return circ

machine.finalize()
