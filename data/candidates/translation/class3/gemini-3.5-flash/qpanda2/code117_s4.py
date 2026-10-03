# EVAL_META: task_id=117, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
import atexit

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    if hasattr(unitary, 'data'):
        matrix = unitary.data
    else:
        matrix = np.array(unitary)
    
    matrix_list = matrix.tolist()
    circuit = pq.matrix_decompose(q, matrix_list)
    return circuit

atexit.register(machine.finalize)
