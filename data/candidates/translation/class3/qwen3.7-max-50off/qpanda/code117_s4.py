# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, alloc_qubits
import numpy as np

def decompose_unitary(unitary):
    q = alloc_qubits(2)
    circ = QCircuit()
    circ.unitary(np.array(unitary, dtype=complex), q)
    return circ
