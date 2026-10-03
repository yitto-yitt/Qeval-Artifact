# EVAL_META: task_id=126, framework=cirq, class=3
import numpy as np
import cirq


def calculate_phase_difference_fidelity():
    # Cirq's Hadamard gate representation
    h_gate = cirq.H
    # Get the unitary matrix of the Hadamard gate
    u_h = cirq.unitary(h_gate)
    # Create the second operator differing by a global phase of exp(i * 0.5)
    global_phase = np.exp(1j * 0.5)
    u_h_phased = global_phase * u_h
    
    # Compute process fidelity
    # process_fidelity = |Tr(U† V)|^2 / d^2
    d = u_h.shape[0]
    trace_val = np.trace(np.conjugate(u_h).T @ u_h_phased)
    fidelity = np.abs(trace_val) ** 2 / d ** 2
    return fidelity
