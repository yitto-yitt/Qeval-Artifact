# EVAL_META: task_id=117, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, matrix_decompose, DecompositionMode

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

    flat = mat.flatten().tolist()

    circuit = matrix_decompose(
        qubits,
        flat,
        DecompositionMode.QSD,
    )
    return circuit


if __name__ == "__main__":
    from pyqpanda import random_qcircuit
    try:
        u = np.eye(4, dtype=complex)
        c = decompose_unitary(u)
        print(c)
    finally:
        machine.finalize()
