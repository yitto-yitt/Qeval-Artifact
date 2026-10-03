# EVAL_META: task_id=126, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def calculate_phase_difference_fidelity():
    op_a = qml.Hadamard(wires=0).matrix()
    op_b = np.exp(1j * 0.5) * qml.Hadamard(wires=0).matrix()
    fidelity = qml.qinfo.process_fidelity(op_a, op_b)
    return fidelity
