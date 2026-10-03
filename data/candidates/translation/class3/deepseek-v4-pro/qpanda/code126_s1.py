# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H

def calculate_phase_difference_fidelity():
    # build Hadamard circuit and get its unitary matrix
    circuit = QCircuit()
    circuit << H(0)
    op_a = circuit.get_matrix()

    # second operator: same unitary with an extra global phase
    op_b = np.exp(1j * 0.5) * op_a

    # process fidelity for two unitaries: |Tr(U† V)| / d
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(np.conjugate(op_a).T @ op_b)) / d
    return fidelity
