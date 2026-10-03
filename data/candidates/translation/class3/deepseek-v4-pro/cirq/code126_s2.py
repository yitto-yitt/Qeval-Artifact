# EVAL_META: task_id=126, framework=cirq, class=3
import numpy as np
import cirq


def calculate_phase_difference_fidelity():
    alpha = 0.5
    phase = np.exp(1j * alpha)

    # U = H, V = e^{i*alpha} H
    # Kraus operators: U = [[U]], V = [[V]]
    # process_fidelity = |Tr(U^\dagger V)|^2 / d^2
    # Here d=2, Tr(U^\dagger V) = Tr(H^\dagger (e^{i*alpha} H)) = e^{i*alpha} * Tr(I) = e^{i*alpha} * 2
    # So fidelity = |2 e^{i*alpha}|^2 / 4 = 4/4 = 1.0
    h = cirq.unitary(cirq.H)
    u = h
    v = phase * h

    # Process fidelity: F = |Tr(U^\dagger V)|^2 / d^2
    d = u.shape[0]
    fidelity = np.abs(np.trace(u.conj().T @ v))**2 / d**2
    return fidelity
