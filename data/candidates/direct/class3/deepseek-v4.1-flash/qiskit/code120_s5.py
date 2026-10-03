# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal

def create_diagonal_circuit(diag):
    gate = Diagonal(diag)
    qc = QuantumCircuit(gate.num_qubits)
    qc.append(gate, range(gate.num_qubits))
    return qc
