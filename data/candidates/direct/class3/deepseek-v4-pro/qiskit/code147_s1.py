# EVAL_META: task_id=147, framework=qiskit, class=3

import numpy as np
from qiskit.circuit.library import MCRY

def mcy(qc):
    """
    Applies a multi-controlled Y gate to qubit 4, with control qubits 0 to 3.
    """
    qc.append(MCRY(np.pi, num_ctrl_qubits=4), range(5))
    return qc
