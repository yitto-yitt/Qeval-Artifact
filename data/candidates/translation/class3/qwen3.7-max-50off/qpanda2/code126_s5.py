# EVAL_META: task_id=126, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    op_a = H
    op_b = np.exp(1j * 0.5) * H
    
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b))**2 / (d**2)
    
    return float(fidelity)

machine.finalize()
