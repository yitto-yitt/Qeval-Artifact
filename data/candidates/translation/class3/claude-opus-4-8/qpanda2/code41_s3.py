# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np

def compose_op():
    I2 = np.eye(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    op = np.eye(2**3, dtype=complex)

    # Pauli "YX": Y on qubit 1, X on qubit 0 -> Y (X) X
    yx = np.kron(Y, X)

    # Embed yx (2 qubits) onto qargs [0, 2] of a 3-qubit space.
    # qargs=[0,2] means yx qubit0 -> system qubit0, yx qubit1 -> system qubit2.
    embedded = np.zeros((8, 8), dtype=complex)

    def bit(x, i):
        return (x >> i) & 1

    def setbit(x, i, v):
        return (x & ~(1 << i)) | (v << i)

    for i in range(8):
        for j in range(8):
            # decompose system indices into (q0,q1,q2)
            i0, i1, i2 = bit(i, 0), bit(i, 1), bit(i, 2)
            j0, j1, j2 = bit(j, 0), bit(j, 1), bit(j, 2)
            # q1 must match (identity)
            if i1 != j1:
                continue
            # yx indices: subsystem qubit0=system q0, subsystem qubit1=system q2
            yi = (i2 << 1) | i0
            yj = (j2 << 1) | j0
            embedded[i, j] = yx[yi, yj]

    # front=True: op.compose(yx, front=True) = op @ yx
    result = op @ embedded
    return result

if __name__ == "__main__":
    print(compose_op())
