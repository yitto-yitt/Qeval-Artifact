# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal

def create_diagonal_circuit(diag):
    n = len(diag).bit_length() - 1
    qc = QuantumCircuit(n)
    qc.append(Diagonal(diag), range(n))
    return qc
