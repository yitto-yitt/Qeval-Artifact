# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit

def remove_gate_in_position(circuit, position):
    if not isinstance(circuit, QuantumCircuit):
        raise TypeError("circuit must be a QuantumCircuit")
    if not isinstance(position, int):
        raise TypeError("position must be an integer")
    if position < 0 or position >= len(circuit.data):
        raise IndexError("position out of range")

    new_circuit = circuit.copy()
    del new_circuit.data[position]
    return new_circuit
