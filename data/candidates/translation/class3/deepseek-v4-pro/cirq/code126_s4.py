# EVAL_META: task_id=126, framework=cirq, class=3
import numpy as np
import cirq


def calculate_phase_difference_fidelity():
    op_a = cirq.unitary(cirq.H)
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    pauli_basis = [np.eye(2), np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]])]
    chi_a = np.zeros((d**2, d**2), dtype=complex)
    chi_b = np.zeros((d**2, d**2), dtype=complex)
    for i, Pi in enumerate(pauli_basis):
        for j, Pj in enumerate(pauli_basis):
            chi_a[i, j] = np.trace(Pi.conj().T @ op_a @ Pj.conj().T @ op_a.conj().T) / d
            chi_b[i, j] = np.trace(Pi.conj().T @ op_b @ Pj.conj().T @ op_b.conj().T) / d
    fid = np.real(np.trace(chi_a.conj().T @ chi_b)) / d
    return fid
