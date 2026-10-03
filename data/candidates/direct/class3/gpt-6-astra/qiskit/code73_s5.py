# EVAL_META: task_id=73, framework=qiskit, class=3
from qiskit import QuantumCircuit


def x_measurement(circuit, qubit, clbit):
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
    return circuit
