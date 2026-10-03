# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit

def remove_gate_in_position(circuit, position):
    """Remove the gate at the specified index in the circuit's data."""
    del circuit.data[position]
    return circuit
