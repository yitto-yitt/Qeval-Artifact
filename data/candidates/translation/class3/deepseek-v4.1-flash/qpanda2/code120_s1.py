# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    N = len(diag)
    n = N.bit_length() - 1
    qubits = global_qubits[:n]
    matrix = [[0j for _ in range(N)] for _ in range(N)]
    for i in range(N):
        matrix[i][i] = complex(diag[i])
    gate = QGate("MATRIX", matrix, qubits)
    circuit = QCircuit()
    circuit << gate
    return circuit

machine.finalize()
