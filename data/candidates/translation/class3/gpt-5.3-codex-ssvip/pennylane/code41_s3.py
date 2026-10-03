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
    full = np.zeros((dim, dim), dtype=complex)

    for col in range(dim):
        bits = [(col >> i) & 1 for i in range(n)]
        sub_col = bits[wires[0]] + 2 * bits[wires[1]]
        for sub_row in range(4):
            amp = yx[sub_row, sub_col]
            if amp == 0:
                continue
            out_bits = bits.copy()
            out_bits[wires[0]] = sub_row & 1
            out_bits[wires[1]] = (sub_row >> 1) & 1
            row = sum((out_bits[i] << i) for i in range(n))
            full[row, col] += amp

    return qml.math.matmul(full, op)
