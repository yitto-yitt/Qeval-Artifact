# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *
import math
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    q = qubits[:n]
    circuit = QCircuit()
    circuit.insert(DiagonalMatrix(q, diag))
    return circuit
machine.finalize()
