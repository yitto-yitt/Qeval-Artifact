# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QProg, matrix_decompose, U4, CNOT

def decompose_unitary(unitary):
    if hasattr(unitary, "to_matrix"):
        mat = np.asarray(unitary.to_matrix(), dtype=complex)
    elif hasattr(unitary, "data"):
        mat = np.asarray(unitary.data, dtype=complex)
    else:
        mat = np.asarray(unitary, dtype=complex)

    qubits = [0, 1]
    circuit = matrix_decompose(qubits, mat)

    prog = QProg()
    prog << circuit
    return prog
