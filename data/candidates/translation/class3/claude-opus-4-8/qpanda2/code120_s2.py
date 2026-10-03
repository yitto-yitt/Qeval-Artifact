# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(np.log2(len(diag)))
    U = np.diag(diag)
    used = qubits[:n]
    circ = matrix_decompose(used, U)
    prog = QCircuit()
    prog.insert(circ)
    return prog


if __name__ == "__main__":
    try:
        _ = create_diagonal_circuit([1, 1, 1, -1])
    finally:
        machine.finalize()
