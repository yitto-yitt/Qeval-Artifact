# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_gate_in_position(circuit, position):
    """
    Remove the gate at the specified position in the quantum circuit.

    Args:
        circuit (QuantumCircuit): The input quantum circuit
        position (int): The position of the gate to remove

    Returns:
        QuantumCircuit: A new quantum circuit with the gate at the specified position removed
    """
    # Create a new circuit with the same number of qubits and clbits as the original
    new_circuit = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)
    
    # Get all operations from the original circuit
    instructions = circuit.data
    
    # Rebuild the circuit excluding the instruction at the specified position
    for i, instruction in enumerate(instructions):
        if i != position:
            new_circuit.append(instruction[0], instruction[1], instruction[2])
    
    return new_circuit
