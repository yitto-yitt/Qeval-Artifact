# EVAL_META: task_id=39, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np

def create_uniform_superposition(n):
    if n == 0:
        return np.array([1.0+0j])
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = qvm.qAlloc_many(n)
    prog = pq.QProg()
    for q in qubits:
        prog << pq.H(q)
    return pq.get_state_vec(prog)
