# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, DiagonalMatrix

def create_diagonal_circuit(diag):
    n = (len(diag) - 1).bit_length()
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    qc = QCircuit()
    qc << DiagonalMatrix(qubits, diag)
    return qc
