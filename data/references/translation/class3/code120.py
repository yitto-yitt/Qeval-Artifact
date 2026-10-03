# EVAL_META: task_id=120, framework=qiskit, class=3

from qiskit.circuit.library import Diagonal
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def create_diagonal_circuit(diag):
    diagonal_gate = Diagonal(diag)
    qc = QuantumCircuit(diagonal_gate.num_qubits)
    qc.append(diagonal_gate.to_instruction(), range(diagonal_gate.num_qubits))
    return qc


# ==================================================
