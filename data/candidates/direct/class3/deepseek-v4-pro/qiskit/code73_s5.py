# EVAL_META: task_id=73, framework=qiskit, class=3
from qiskit import QuantumCircuit


def x_measurement(circuit, qubit, clbit):
    """Add an X-basis measurement on the specified qubit to the specified classical bit."""
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
    return circuit
