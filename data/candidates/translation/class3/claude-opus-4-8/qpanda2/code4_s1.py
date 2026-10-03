# EVAL_META: task_id=4, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    flat = [complex(x) for row in matrix for x in row]
    circuit = matrix_decompose(qubits, flat)
    return circuit

if __name__ == "__main__":
    circ = create_unitary_from_matrix()
    print(circ)
    machine.finalize()
