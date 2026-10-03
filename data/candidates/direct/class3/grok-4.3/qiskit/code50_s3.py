# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit

def remove_gate_in_position(circuit, position):
    new_circuit = circuit.copy()
    new_circuit.data.pop(position)
    return new_circuit
