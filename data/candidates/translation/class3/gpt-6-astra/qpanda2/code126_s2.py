# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
_program = pq.QProg()
_program << pq.H(qubits[0])
_hadamard_matrix = np.asarray(pq.get_matrix(_program), dtype=complex).reshape(2, 2)


def calculate_phase_difference_fidelity():
    op_a = _hadamard_matrix
    op_b = np.exp(1j * 0.5) * op_a
    dimension = op_a.shape[0]
    return float(abs(np.trace(op_a.conj().T @ op_b)) ** 2 / dimension**2)


machine.finalize()
