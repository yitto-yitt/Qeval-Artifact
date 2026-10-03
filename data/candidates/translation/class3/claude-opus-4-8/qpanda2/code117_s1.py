# EVAL_META: task_id=117, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def _to_matrix(unitary):
    if hasattr(unitary, "to_matrix"):
        return np.array(unitary.to_matrix(), dtype=complex)
    if hasattr(unitary, "data"):
        return np.array(unitary.data, dtype=complex)
    return np.array(unitary, dtype=complex)


def decompose_unitary(unitary):
    mat = _to_matrix(unitary)
    circuit = matrix_decompose(qubits, mat)
    return circuit


if __name__ == "__main__":
    U = np.array([
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ], dtype=complex)
    circ = decompose_unitary(U)
    prog = QProg()
    prog << circ
    print(prog)
    machine.finalize()
