# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_gate_in_position(circuit, position):
    """
    Removes the gate at the specified position in the quantum circuit.

    Args:
        circuit (QuantumCircuit): The input quantum circuit
        position (int): The position of the gate to remove (0-indexed)

    Returns:
        QuantumCircuit: A new quantum circuit with the gate removed
    """
    # Create a new circuit with the same number of qubits and classical bits
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    
    # Get all operations in the circuit
    instructions = circuit.data
    
    # Validate position
    if position < 0 or position >= len(instructions):
        raise IndexError("Position out of range")
    
    # Add all gates except the one at the specified position
    for i, instruction in enumerate(instructions):
        if i != position:
            new_circuit.append(instruction[0], instruction[1], instruction[2])
    
    return new_circuit
