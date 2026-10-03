# EVAL_META: task_id=6, framework=qiskit, class=2

from qiskit import QuantumCircuit

def create_state_prep(num_qubits: int) -> QuantumCircuit:
    """Return a QuantumCircuit that prepares the state |1> on all qubits of an n-qubit register."""
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        qc.x(i)
    return qc
