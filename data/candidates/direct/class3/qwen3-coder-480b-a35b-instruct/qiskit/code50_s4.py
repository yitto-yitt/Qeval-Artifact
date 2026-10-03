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
    # Create a new quantum circuit with the same number of qubits and classical bits
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)

    # Get all the instructions from the original circuit
    instructions = circuit.data

    # Iterate through the instructions and add all except the one at the specified position
    for i, instruction in enumerate(instructions):
        if i != position:
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)

    return new_circuit
