# EVAL_META: task_id=117, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    circuit = pq.matrix_decompose(qubits, np.array(unitary))
    return circuit

machine.finalize()
