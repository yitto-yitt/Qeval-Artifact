# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np


def compose_op():
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    op = np.eye(2 ** 3, dtype=complex)

    # Pauli "YX": label index 0 -> qubit 0 -> X, label index 1 -> qubit 1 -> Y
    yx = np.kron(Y, X)

    n = 3
    qargs = [0, 2]

    def embed(mat, qubits, num_qubits):
        full = None
        # build operator acting on full system, qubit 0 = least significant
        ops = [I2] * num_qubits
        sub_dim = int(np.log2(mat.shape[0]))
        # decompose two-qubit gate by full tensor construction
        full_mat = np.zeros((2 ** num_qubits, 2 ** num_qubits), dtype=complex)
        for i in range(2 ** num_qubits):
            for j in range(2 ** num_qubits):
                # extract sub-indices for qargs
                sub_i = 0
                sub_j = 0
                match = True
                for q in range(num_qubits):
                    bi = (i >> q) & 1
                    bj = (j >> q) & 1
                    if q in qubits:
                        pos = qubits.index(q)
                        sub_i |= (bi << pos)
                        sub_j |= (bj << pos)
                    else:
                        if bi != bj:
                            match = False
                            break
                if match:
                    full_mat[i, j] = mat[sub_i, sub_j]
        return full_mat

    yx_full = embed(yx, qargs, n)

    # front=True: result = op.compose(yx, front=True) = op @ yx
    result = op @ yx_full
    return result
