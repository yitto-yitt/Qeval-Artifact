# EVAL_META: task_id=73, framework=qiskit, class=3
from qiskit import QuantumCircuit


def x_measurement(circuit: QuantumCircuit, qubit: int, clbit: int) -> QuantumCircuit:
    """Add an X-basis measurement on `qubit`, storing the result to `clbit`."""
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
    return circuit
