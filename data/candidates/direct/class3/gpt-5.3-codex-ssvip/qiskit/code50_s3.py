# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit

def remove_gate_in_position(circuit, position):
    if not isinstance(circuit, QuantumCircuit):
        raise TypeError("circuit must be a QuantumCircuit")
    n_ops = len(circuit.data)
    if position < 0 or position >= n_ops:
        raise IndexError("position out of range")
    del circuit.data[position]
    return circuit
