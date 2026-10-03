# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init()
qvec = machine.qAlloc_many(64)

def qft_no_swaps(num_qubits):
    circuit = pq.QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            angle = -np.pi / (2 ** (k - j))
            circuit << pq.CU1(qvec[k], qvec[j], angle)
        circuit << pq.H(qvec[j])
    return circuit

machine.finalize()
