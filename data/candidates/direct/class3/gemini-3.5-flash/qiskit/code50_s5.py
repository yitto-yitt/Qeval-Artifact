# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit

def remove_gate_in_position(circuit: QuantumCircuit, position: int) -> QuantumCircuit:
    """Remove the gate in the input position for the given Quantum Circuit."""
    circuit.data.pop(position)
    return circuit
