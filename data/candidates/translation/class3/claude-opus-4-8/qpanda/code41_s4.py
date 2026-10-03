# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np


def compose_op():
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    op = np.eye(2 ** 3, dtype=complex)

    yx = np.kron(Y, X)

    embed = np.eye(2 ** 3, dtype=complex)
    embed_map = {}

    dim = 2 ** 3
    result = np.zeros((dim, dim), dtype=complex)

    def bit(state, q):
        return (state >> q) & 1

    def set_bit(state, q, val):
        if val:
            return state | (1 << q)
        else:
            return state & ~(1 << q)

    yx_full = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        b0 = bit(col, 0)
        b2 = bit(col, 2)
        for r0 in range(2):
            for r2 in range(2):
                amp = yx[(r2 << 1) | r0, (b2 << 1) | b0]
                if amp != 0:
                    row = col
                    row = set_bit(row, 0, r0)
                    row = set_bit(row, 2, r2)
                    yx_full[row, col] += amp

    composed = op.dot(yx_full)
    return composed
