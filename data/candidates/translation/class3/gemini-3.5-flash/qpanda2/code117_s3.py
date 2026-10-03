# EVAL_META: task_id=117, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

# Global QVM
machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    if hasattr(unitary, 'data'):
        matrix = unitary.data
    else:
        matrix = np.array(unitary)
    
    matrix_list = [[complex(x) for x in row] for row in matrix]
    circuit = pq.matrix_decompose(global_qubits, matrix_list)
    return circuit

machine.finalize()
