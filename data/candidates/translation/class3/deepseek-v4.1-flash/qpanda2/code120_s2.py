# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QOracle

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    if 2**n != len(diag):
        raise ValueError("Length of diag must be a power of 2")
    circuit = QCircuit()
    if n == 0:
        return circuit
    q = qubits[:n]
    matrix = np.diag(diag)
    matrix_list = [[complex(x) for x in row] for row in matrix]
    circuit << QOracle(q, matrix_list)
    return circuit

if __name__ == "__main__":
    machine.finalize()
