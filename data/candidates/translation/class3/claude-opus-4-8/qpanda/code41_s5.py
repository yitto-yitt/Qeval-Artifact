# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np


def compose_op():
    I2 = np.eye(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    yx = np.kron(Y, X)

    op = np.eye(2 ** 3, dtype=complex)

    qargs = [0, 2]
    num_qubits = 3
    embed = np.eye(1, dtype=complex)
    yx_qubits = list(reversed(qargs))
    full = None

    def embed_operator(sub, sub_qubits, total):
        dim = 2 ** total
        result = np.zeros((dim, dim), dtype=complex)
        n_sub = len(sub_qubits)
        for i in range(dim):
            bits_i = [(i >> b) & 1 for b in range(total)]
            for j in range(dim):
                bits_j = [(j >> b) & 1 for b in range(total)]
                ok = True
                for b in range(total):
                    if b not in sub_qubits and bits_i[b] != bits_j[b]:
                        ok = False
                        break
                if not ok:
                    continue
                sub_i = 0
                sub_j = 0
                for idx, qb in enumerate(sub_qubits):
                    sub_i |= bits_i[qb] << idx
                    sub_j |= bits_j[qb] << idx
                result[i, j] = sub[sub_i, sub_j]
        return result

    yx_embedded = embed_operator(yx, qargs, num_qubits)

    result = yx_embedded @ op
    return result
