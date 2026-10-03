# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import DiagonalGate
import math

def create_diagonal_circuit(diag):
    n = (len(diag).bit_length() - 1) if len(diag) > 0 else 0
    qc = QuantumCircuit(n)
    qc.append(DiagonalGate(diag), list(range(n)))
    return qc
