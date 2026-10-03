# EVAL_META: task_id=117, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, matrix_decompose, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def decompose_unitary(unitary):
    if hasattr(unitary, 'data'):
        mat = np.array(unitary.data, dtype=complex)
    else:
        mat = np.array(unitary, dtype=complex)

    mat_list = [[complex(mat[i, j]) for j in range(mat.shape[1])]
                for i in range(mat.shape[0])]

    circuit = matrix_decompose(qubits, mat_list)
    return circuit
