# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def calculate_phase_difference_fidelity():
    H = (1.0 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
    op_a = H
    op_b = np.exp(1j * 0.5) * H
    d = op_a.shape[0]
    overlap = np.trace(op_a.conj().T @ op_b)
    fidelity = np.abs(overlap) ** 2 / (d ** 2)
    return fidelity


if __name__ == "__main__":
    print(calculate_phase_difference_fidelity())
    machine.finalize()
