# EVAL_META: task_id=120, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    if n == 0:
        return pq.QCircuit()
    matrix = np.diag(diag)
    qubits = [q[i] for i in range(n)]
    return pq.matrix_decompose(qubits, matrix)

atexit.register(machine.finalize)
