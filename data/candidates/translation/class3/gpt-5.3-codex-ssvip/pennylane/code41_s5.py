# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    op = np.eye(2**3, dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    yx = np.kron(y, x)

    wires = [0, 2]
    n = 3
    dim = 2**n
    embedded = np.zeros((dim, dim), dtype=complex)

    for col in range(dim):
        bits_col = [(col >> (n - 1 - w)) & 1 for w in range(n)]
        local_col = (bits_col[wires[0]] << 1) | bits_col[wires[1]]
        for local_row in range(4):
            amp = yx[local_row, local_col]
            if amp == 0:
                continue
            bits_row = bits_col.copy()
            bits_row[wires[0]] = (local_row >> 1) & 1
            bits_row[wires[1]] = local_row & 1
            row = 0
            for b in bits_row:
                row = (row << 1) | b
            embedded[row, col] += amp

    return embedded @ op
