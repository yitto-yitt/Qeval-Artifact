# EVAL_META: task_id=50, framework=qiskit, class=3

from qiskit import QuantumCircuit

def remove_gate_in_position(circuit: QuantumCircuit, position: int) -> QuantumCircuit:
    """Remove the gate at the specified position in the QuantumCircuit."""
    circuit.data.pop(position)
    return circuit
