# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
program = pq.QProg()
program << pq.H(qubits[0])
hadamard_matrix = np.array(pq.get_matrix(program), dtype=complex).reshape(2, 2)


def calculate_phase_difference_fidelity():
    op_a = hadamard_matrix
    op_b = np.exp(1j * 0.5) * op_a
    dimension = op_a.shape[0]
    return float(np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / dimension**2)


machine.finalize()
