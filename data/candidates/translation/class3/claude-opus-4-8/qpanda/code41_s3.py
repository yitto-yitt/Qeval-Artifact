# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np


def compose_op():
    op = np.eye(2 ** 3)

    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    yx = np.kron(Y, X)

    full = np.eye(2 ** 3, dtype=complex)
    qargs = [0, 2]
    num_qubits = 3
    dims = [2] * num_qubits
    embedded = np.zeros((2 ** num_qubits, 2 ** num_qubits), dtype=complex)

    for i in range(2 ** num_qubits):
        for j in range(2 ** num_qubits):
            ibits = [(i >> b) & 1 for b in range(num_qubits)]
            jbits = [(j >> b) & 1 for b in range(num_qubits)]
            rest_i = [ibits[b] for b in range(num_qubits) if b not in qargs]
            rest_j = [jbits[b] for b in range(num_qubits) if b not in qargs]
            if rest_i != rest_j:
                continue
            sub_i = 0
            sub_j = 0
            for idx, q in enumerate(qargs):
                sub_i |= ibits[q] << idx
                sub_j |= jbits[q] << idx
            embedded[i, j] = yx[sub_i, sub_j]

    result = op @ embedded
    return result
