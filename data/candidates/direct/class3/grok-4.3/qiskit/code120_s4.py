# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import DiagonalGate

def create_diagonal_circuit(diag):
    num_qubits = (len(diag).bit_length() - 1)
    qc = QuantumCircuit(num_qubits)
    qc.append(DiagonalGate(diag), range(num_qubits))
    return qc
