# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    op = np.eye(2**3, dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    yx = np.kron(y, x)

    composed = np.zeros_like(op, dtype=complex)
    qargs = [0, 2]

    for col in range(2**3):
        in_bits = [(col >> i) & 1 for i in range(3)]
        local_col = sum(in_bits[qargs[i]] << i for i in range(2))

        for local_row in range(2**2):
            amp = yx[local_row, local_col]
            if amp == 0:
                continue

            out_bits = in_bits.copy()
            for i in range(2):
                out_bits[qargs[i]] = (local_row >> i) & 1

            row = sum(out_bits[i] << i for i in range(3))
            composed[row, col] = amp

    return qml.QubitUnitary(composed, wires=[0, 1, 2])
