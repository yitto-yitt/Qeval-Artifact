# EVAL_META: task_id=117, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, matrix_decompose, QMatrixToOMatrix

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def decompose_unitary(unitary):
    if hasattr(unitary, "data"):
        mat = np.array(unitary.data, dtype=complex)
    elif hasattr(unitary, "to_matrix"):
        mat = np.array(unitary.to_matrix(), dtype=complex)
    else:
        mat = np.array(unitary, dtype=complex)

    flat = []
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            flat.append(complex(mat[i, j]))

    circuit = matrix_decompose(qubits, flat)
    return circuit


if __name__ == "__main__":
    from pyqpanda import random_qcircuit
    U = np.eye(4, dtype=complex)
    circ = decompose_unitary(U)
    print(circ)
    machine.finalize()
