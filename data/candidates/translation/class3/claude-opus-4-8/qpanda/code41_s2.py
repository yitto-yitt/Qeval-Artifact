# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np


def compose_op():
    I2 = np.eye(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    op = np.eye(2 ** 3, dtype=complex)

    yx = np.kron(Y, X)

    def embed(two_qubit_mat, qargs, num_qubits):
        full = np.zeros((2 ** num_qubits, 2 ** num_qubits), dtype=complex)
        dim = 2 ** num_qubits
        for i in range(dim):
            for j in range(dim):
                bi = [(i >> k) & 1 for k in range(num_qubits)]
                bj = [(j >> k) & 1 for k in range(num_qubits)]
                other = True
                for k in range(num_qubits):
                    if k in qargs:
                        continue
                    if bi[k] != bj[k]:
                        other = False
                        break
                if not other:
                    continue
                sub_i = 0
                sub_j = 0
                for idx, q in enumerate(qargs):
                    sub_i |= bi[q] << idx
                    sub_j |= bj[q] << idx
                full[i, j] = two_qubit_mat[sub_i, sub_j]
        return full

    yx_embedded = embed(yx, [0, 2], 3)

    result = op @ yx_embedded
    return result
