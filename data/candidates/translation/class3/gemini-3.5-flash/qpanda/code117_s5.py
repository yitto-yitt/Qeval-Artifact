# EVAL_META: task_id=117, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def decompose_unitary(unitary):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    u_arr = np.array(unitary)
    qstat = u_arr.flatten().tolist()
    
    circuit = pq.matrix_decompose(qubits, qstat)
    return circuit
