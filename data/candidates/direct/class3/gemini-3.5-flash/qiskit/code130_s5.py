# EVAL_META: task_id=130, framework=qiskit, class=3

from qiskit import QuantumCircuit

def inv_circuit(n: int) -> QuantumCircuit:
    """
    Create a quantum circuit with 'n' qubits.
    Apply Hadamard gates to the second and third qubits (indices 1 and 2).
    Then apply CNOT gates between the second and fourth qubits (indices 1 and 3),
    and between the third and fifth qubits (indices 2 and 4).
    Finally, return the inverse of the quantum circuit.
    """
    qc = QuantumCircuit(n)
    # Apply Hadamard gates to the second and third qubits (0-indexed: 1 and 2)
    qc.h(1)
    qc.h(2)
    # Apply CNOT between second and fourth qubits (0-indexed: 1 and 3)
    qc.cx(1, 3)
    # Apply CNOT between third and fifth qubits (0-indexed: 2 and 4)
    qc.cx(2, 4)
    # Return the inverse of the circuit
    return qc.inverse()
