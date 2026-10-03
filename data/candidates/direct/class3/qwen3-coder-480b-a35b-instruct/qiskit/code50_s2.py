# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_gate_in_position(circuit, position):
    """
    Remove the gate at the specified position in the quantum circuit.

    Args:
        circuit (QuantumCircuit): The input quantum circuit
        position (int): The position of the gate to remove

    Returns:
        QuantumCircuit: A new quantum circuit with the gate removed
    """
    # Create a new circuit with the same number of qubits and clbits
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    
    # Get all instructions except the one at the specified position
    for i, instruction in enumerate(circuit.data):
        if i != position:
            new_circuit.append(instruction[0], instruction[1], instruction[2])
    
    return new_circuit
