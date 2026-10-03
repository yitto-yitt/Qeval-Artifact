# EVAL_META: task_id=126, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def calculate_phase_difference_fidelity():
    op_a = qml.Hadamard(wires=0).matrix()
    op_b = np.exp(1j * 0.5) * qml.Hadamard(wires=0).matrix()
    d = 2
    fidelity = np.abs(np.trace(np.dot(op_a.conj().T, op_b)))**2 / d**2
    return fidelity
