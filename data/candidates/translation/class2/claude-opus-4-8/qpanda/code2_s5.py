# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, QProg, H, CNOT

import numpy as np


def create_bell_statevector():
    qc = QCircuit(2)
    qc << H(0)
    qc << CNOT(0, 1)

    prog = QProg()
    prog << qc

    state = prog.statevector()
    return np.array(state, dtype=complex)
