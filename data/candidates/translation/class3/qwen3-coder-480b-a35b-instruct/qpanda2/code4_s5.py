# EVAL_META: task_id=4, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    matrix_np = np.array(matrix, dtype=complex)
    
    prog = pq.QProg()
    prog.insert(pq.unitary_single_opt(qubits[0], qubits[1], matrix_np))
    
    return prog

prog_result = create_unitary_from_matrix()
machine.finalize()
