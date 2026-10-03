# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_gate_in_position(circuit, position):
    result = circuit.copy()
    del result.data[position]
    return result
