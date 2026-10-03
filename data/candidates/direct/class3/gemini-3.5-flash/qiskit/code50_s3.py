# EVAL_META: task_id=50, framework=qiskit, class=3

from qiskit import QuantumCircuit

def remove_gate_in_position(circuit: QuantumCircuit, position: int) -> QuantumCircuit:
    """Remove the gate at the specified position (index) in the Quantum Circuit.

    Args:
        circuit (QuantumCircuit): The input quantum circuit.
        position (int): The index of the gate to remove.

    Returns:
        QuantumCircuit: The modified quantum circuit.
    """
    circuit.data.pop(position)
    return circuit
