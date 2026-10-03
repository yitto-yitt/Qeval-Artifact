# EVAL_META: task_id=3, framework=qiskit, class=2

from qiskit import QuantumCircuit


def create_ghz(drawing=False):
    circuit = QuantumCircuit(3, 3)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(0, 2)
    circuit.measure([0, 1, 2], [0, 1, 2])

    if drawing:
        return circuit, circuit.draw(output="mpl")
    return circuit
