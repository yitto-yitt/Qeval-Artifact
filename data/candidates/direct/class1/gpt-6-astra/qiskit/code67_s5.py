# EVAL_META: task_id=67, framework=qiskit, class=1
from math import pi
from qiskit import QuantumCircuit


def chsh_circuit(alice, bob):
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)

    if alice == 1:
        circuit.h(0)
    circuit.ry(-pi / 4 if bob == 0 else pi / 4, 1)

    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit
