# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import Clifford


def equivalent_clifford_circuit(circuit, n):
    target = np.array(circuit, dtype=complex)
    if target.ndim != 2 or target.shape[0] != target.shape[1]:
        raise ValueError("circuit must be a square unitary matrix or matrix-like object.")
    dim = target.shape[0]
    num_qubits = int(round(np.log2(dim)))
    if 2 ** num_qubits != dim:
        raise ValueError("Matrix dimension must be a power of 2.")

    qc_list = []
    while len(qc_list) < n:
        c = Clifford.random_clifford(num_qubits)
        u = np.array(c.matrix(), dtype=complex)
        if np.allclose(u, target, rtol=0.4, atol=0.4):
            qc_list.append(c)
    return qc_list
