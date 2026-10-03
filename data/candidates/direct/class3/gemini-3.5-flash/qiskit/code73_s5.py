# EVAL_META: task_id=73, framework=qiskit, class=3
from qiskit import QuantumCircuit

def x_measurement(circuit: QuantumCircuit, qubit, clbit) -> QuantumCircuit:
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
    return circuit
