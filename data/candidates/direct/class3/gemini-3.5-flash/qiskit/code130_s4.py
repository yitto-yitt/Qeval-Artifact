# EVAL_META: task_id=130, framework=qiskit, class=3

from qiskit import QuantumCircuit

def inv_circuit(n: int) -> QuantumCircuit:
    """
    Creates a quantum circuit with 'n' qubits, applies Hadamard gates to the second
    and third qubits, CNOT gates between the second and fourth qubits, and between
    the third and fifth qubits. Returns the inverse of this circuit.
    """
    qc = QuantumCircuit(n)
    
    # Apply Hadamard gates to the second (index 1) and third (index 2) qubits
    qc.h(1)
    qc.h(2)
    
    # Apply CNOT between the second (index 1) and fourth (index 3) qubits
    qc.cx(1, 3)
    
    # Apply CNOT between the third (index 2) and fifth (index 4) qubits
    qc.cx(2, 4)
    
    # Return the inverse of the circuit
    return qc.inverse()
