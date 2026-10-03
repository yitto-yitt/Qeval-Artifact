# EVAL_META: task_id=117, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def decompose_unitary(unitary):
    if hasattr(unitary, "data"):
        unitary = unitary.data
    elif hasattr(unitary, "to_matrix"):
        unitary = unitary.to_matrix()
        
    if isinstance(unitary, np.ndarray):
        unitary_list = unitary.flatten().tolist()
    else:
        unitary_list = [val for row in unitary for val in row]
        
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    
    circuit = pq.matrix_decompose(q, unitary_list)
    return circuit
