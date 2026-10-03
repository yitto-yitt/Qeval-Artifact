# EVAL_META: task_id=126, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def calculate_phase_difference_fidelity():
    h_gate = pq.H(qubits[0])

    try:
        h_matrix = h_gate.get_matrix()
    except AttributeError:
        h_matrix = pq.get_matrix(h_gate)

    op_a = np.asarray(h_matrix, dtype=complex)
    if op_a.ndim == 1:
        op_a = op_a.reshape((2, 2))

    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (dim * dim)
    return float(np.real_if_close(np.clip(fidelity.real, 0.0, 1.0)))
