# EVAL_META: task_id=105, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, CNOT, T, get_matrix

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def initialize_cnot_dihedral():
    circ = QCircuit()
    circ << CNOT(qubits[0], qubits[1])
    circ << T(qubits[0])
    matrix = get_matrix(circ)
    return np.array(matrix).reshape(4, 4)


result = initialize_cnot_dihedral()
machine.finalize()
