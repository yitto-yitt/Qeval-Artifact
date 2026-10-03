# EVAL_META: task_id=0, framework=qiskit, class=3

from qiskit import QuantumCircuit

def create_quantum_circuit(n_qubits: int) -> QuantumCircuit:
    """
    Generates a Quantum Circuit for the given number of qubits.
    
    Args:
        n_qubits (int): The number of qubits in the circuit.
        
    Returns:
        QuantumCircuit: The created Qiskit QuantumCircuit object.
    """
    return QuantumCircuit(n_qubits)
