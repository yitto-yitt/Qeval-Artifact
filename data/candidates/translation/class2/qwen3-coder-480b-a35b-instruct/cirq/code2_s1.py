# EVAL_META: task_id=2, framework=cirq, class=2
import cirq
import numpy as np


def create_bell_statevector():
    # Create the Phi+ Bell state: (|00⟩ + |11⟩) / √2
    phi_plus = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    return cirq.StateVectorSimulationState(phi_plus)
