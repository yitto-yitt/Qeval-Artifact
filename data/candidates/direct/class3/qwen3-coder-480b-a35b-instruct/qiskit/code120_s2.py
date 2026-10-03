# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal

def create_diagonal_circuit(diag):
    n_qubits = len(diag).bit_length() - 1  # Calculate number of qubits needed
    qc = QuantumCircuit(n_qubits)
    qc.append(Diagonal(diag), range(n_qubits))
    return qc
