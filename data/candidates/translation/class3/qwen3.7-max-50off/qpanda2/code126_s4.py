# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    op_a = H
    op_b = np.exp(1j * 0.5) * H
    
    d = 2
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b))**2 / (d**2)
    
    return float(fidelity)

machine.finalize()
