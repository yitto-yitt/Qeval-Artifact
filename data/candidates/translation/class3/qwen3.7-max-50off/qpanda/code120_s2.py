# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit
try:
    from pyqpanda3.core import Diagonal
except ImportError:
    from pyqpanda3.core.gate import Diagonal

def create_diagonal_circuit(diag):
    n = len(diag).bit_length() - 1
    qubits = [Qubit() for _ in range(n)]
    qc = QCircuit()
    qc.insert(Diagonal(qubits, diag))
    return qc
