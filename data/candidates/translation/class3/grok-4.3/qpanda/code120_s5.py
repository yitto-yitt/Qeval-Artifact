# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import Diagonal
from pyqpanda3.core import Circuit

def create_diagonal_circuit(diag):
    diagonal_gate = Diagonal(diag)
    qc = Circuit(diagonal_gate.num_qubits)
    qc.append(diagonal_gate.to_instruction(), range(diagonal_gate.num_qubits))
    return qc
