# EVAL_META: task_id=4, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [1, 0, 0, 0],
                       [0, 1, 0, 0]], dtype=complex)
    circuit = matrix_decompose(qubits, matrix)
    return circuit


if __name__ == "__main__":
    circ = create_unitary_from_matrix()
    print(circ)
    machine.finalize()
