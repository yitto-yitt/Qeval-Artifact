# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, QOracle

_QVM = CPUQVM()
if hasattr(_QVM, "init"):
    _QVM.init()
else:
    _QVM.init_qvm()


def create_diagonal_circuit(diag):
    n = (len(diag) - 1).bit_length()
    if n == 0:
        return QCircuit()

    size = 1 << n
    matrix = [[0j] * size for _ in range(size)]
    for i, value in enumerate(diag):
        matrix[i][i] = value

    oracle = QOracle(matrix)
    qubits = _QVM.qAlloc_many(n)

    if hasattr(oracle, "generate_circuit"):
        return oracle.generate_circuit(qubits)
    else:
        return oracle.generateCircuit(qubits)
