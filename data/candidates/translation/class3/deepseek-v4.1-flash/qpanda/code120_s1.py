# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, Diagonal

def create_diagonal_circuit(diag):
    n = len(diag).bit_length() - 1
    qubits = [Qubit(i) for i in range(n)]
    circuit = QCircuit()
    circuit << Diagonal(qubits, diag)
    return circuit
